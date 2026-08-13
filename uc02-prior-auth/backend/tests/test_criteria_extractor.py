import pytest
from unittest.mock import AsyncMock, patch
from app.models.policy import PolicyChunk
from app.models.criteria import PolicyCriteriaOutput
from app.services import criteria_extractor

@pytest.fixture
def sample_chunk():
    return PolicyChunk(
        source_type="PAYER",
        source_name="Anthem",
        policy_name="Lumbar MRI Policy",
        source_file="lumbar_mri.pdf",
        page_number=6,
        section="Medical Necessity",
        text="Conservative therapy attempted for at least 6 weeks is required.",
        chunk_index=0
    )

@pytest.mark.anyio
async def test_extract_policy_criteria_empty_chunks():
    result = await criteria_extractor.extract_policy_criteria([])
    assert isinstance(result, PolicyCriteriaOutput)
    assert result.policy_name == "Unknown Policy"
    assert len(result.criteria) == 0

@pytest.mark.anyio
async def test_extract_policy_criteria_success(sample_chunk):
    mock_llm_json = """{
      "policy_name": "Lumbar MRI Policy",
      "criteria": [
        {
          "criterion_id": "C1",
          "description": "Conservative therapy attempted for at least 6 weeks",
          "required": true,
          "operator": ">=",
          "required_value": 6.0,
          "unit": "weeks",
          "source_page": 6,
          "source_section": "Medical Necessity"
        }
      ]
    }"""

    with patch("app.services.llm_client.generate_response", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = mock_llm_json
        
        result = await criteria_extractor.extract_policy_criteria([(sample_chunk, 0.90)])
        
        assert isinstance(result, PolicyCriteriaOutput)
        assert result.policy_name == "Lumbar MRI Policy"
        assert len(result.criteria) == 1
        
        c = result.criteria[0]
        assert c.criterion_id == "C1"
        assert c.description == "Conservative therapy attempted for at least 6 weeks"
        assert c.required is True
        assert c.operator == ">="
        assert c.required_value == 6.0
        assert c.unit == "weeks"
        assert c.source_page == 6
        assert c.source_section == "Medical Necessity"

@pytest.mark.anyio
async def test_extract_policy_criteria_validation_error(sample_chunk):
    # LLM returns invalid json format
    mock_llm_invalid = "This is not json text"

    with patch("app.services.llm_client.generate_response", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = mock_llm_invalid
        
        with pytest.raises(ValueError):
            await criteria_extractor.extract_policy_criteria([(sample_chunk, 0.90)])
