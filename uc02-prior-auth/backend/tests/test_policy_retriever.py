import pytest
from unittest.mock import AsyncMock, patch
from app.models.policy import PolicyChunk
from app.services import policy_retriever

@pytest.fixture
def mock_chunks():
    return [
        PolicyChunk(
            source_type="PAYER",
            source_name="Anthem",
            policy_name="MRI Policy",
            source_file="mri_policy.pdf",
            page_number=1,
            section="Description",
            text="Anthem policy text for MRI procedures.",
            chunk_index=0,
            cpt_codes=["72148"]
        ),
        PolicyChunk(
            source_type="PAYER",
            source_name="Uhc",
            policy_name="Wrist Surgery Policy",
            source_file="wrist_policy.pdf",
            page_number=2,
            section="Medical Necessity",
            text="UHC requirements for wrist surgery and thumb repair.",
            chunk_index=1,
            cpt_codes=["25441"]
        ),
        PolicyChunk(
            source_type="PAYER",
            source_name="Anthem",
            policy_name="Knee Policy",
            source_file="knee_policy.pdf",
            page_number=3,
            section="Clinical Criteria",
            text="General Anthem policy text.",
            chunk_index=2,
            cpt_codes=[]
        )
    ]

@pytest.mark.anyio
async def test_retrieve_unknown_payer():
    result = await policy_retriever.retrieve_relevant_policies(
        payer=None,
        diagnosis="Chronic pain",
        procedure="MRI"
    )
    assert result.status == "PAYER_UNKNOWN"
    assert len(result.chunks) == 0

@pytest.mark.anyio
async def test_retrieve_payer_isolation(mock_chunks):
    # Mock search_vector_store to return all mock chunks with same base similarity score
    mock_search = [(chunk, 0.40) for chunk in mock_chunks]
    
    with patch("app.services.policy_retriever.search_vector_store", new_callable=AsyncMock) as mock_search_store:
        mock_search_store.return_value = mock_search
        
        # Test Anthem retrieval
        result = await policy_retriever.retrieve_relevant_policies(
            payer="Anthem",
            diagnosis="Chronic back pain",
            procedure="Lumbar MRI",
            cpt_code="72148"
        )
        
        assert result.status == "SUCCESS"
        assert len(result.chunks) > 0
        for chunk, score in result.chunks:
            assert chunk.source_name == "Anthem"

@pytest.mark.anyio
async def test_retrieve_cpt_code_boosting(mock_chunks):
    # Both Anthem chunks are returned with identical baseline vector scores of 0.40
    anthem_chunks = [c for c in mock_chunks if c.source_name == "Anthem"]
    mock_search = [(chunk, 0.40) for chunk in anthem_chunks]

    with patch("app.services.policy_retriever.search_vector_store", new_callable=AsyncMock) as mock_search_store:
        mock_search_store.return_value = mock_search
        
        # Request CPT code "72148" (which only the first chunk has in its cpt_codes metadata)
        result = await policy_retriever.retrieve_relevant_policies(
            payer="Anthem",
            diagnosis="Chronic back pain",
            procedure="Lumbar MRI",
            cpt_code="72148"
        )
        
        assert result.status == "SUCCESS"
        # The matching chunk should be boosted and ranked first
        first_chunk, score1 = result.chunks[0]
        second_chunk, score2 = result.chunks[1]
        
        assert "72148" in first_chunk.cpt_codes
        assert "72148" not in second_chunk.cpt_codes
        assert score1 > score2  # verify boost was applied

@pytest.mark.anyio
async def test_retrieve_insufficient_evidence_threshold(mock_chunks):
    # Returns very low baseline vector similarity score
    mock_search = [(chunk, 0.01) for chunk in mock_chunks]

    with patch("app.services.policy_retriever.search_vector_store", new_callable=AsyncMock) as mock_search_store:
        mock_search_store.return_value = mock_search
        
        result = await policy_retriever.retrieve_relevant_policies(
            payer="Uhc",
            diagnosis="Severe pain",
            procedure="Sleep study",
            cpt_code="99999"  # code not matching wrist policy
        )
        
        assert result.status == "INSUFFICIENT_POLICY_EVIDENCE"
        assert len(result.chunks) == 0
