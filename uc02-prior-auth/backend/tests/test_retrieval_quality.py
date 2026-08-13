import pytest
from unittest.mock import AsyncMock, patch
from app.models.policy import PolicyChunk
from app.services import policy_retriever

@pytest.fixture
def mock_candidates():
    return [
        # Two duplicate content chunks (from same or different parts)
        PolicyChunk(
            source_type="PAYER",
            source_name="Anthem",
            policy_name="MRI Policy",
            source_file="mri.pdf",
            page_number=1,
            section="Description",
            text="Identical text body content.",
            chunk_index=0
        ),
        PolicyChunk(
            source_type="PAYER",
            source_name="Anthem",
            policy_name="MRI Policy 2",
            source_file="mri_2.pdf",
            page_number=2,
            section="Medical Necessity",
            text="Identical text body content.",
            chunk_index=1
        ),
        # Unique content chunk with different section & policy ID
        PolicyChunk(
            source_type="PAYER",
            source_name="Anthem",
            policy_name="Obesity Policy",
            policy_id="CG-SURG-83",
            source_file="obesity.pdf",
            page_number=3,
            section="Medical Necessity",
            text="Medically necessary details for bariatric care.",
            chunk_index=2
        )
    ]

@pytest.mark.anyio
async def test_retrieval_suppress_duplicates(mock_candidates):
    # Retrieve all candidate chunks with scores
    mock_search = [(c, 0.50) for c in mock_candidates]
    
    with patch("app.services.policy_retriever.search_vector_store", new_callable=AsyncMock) as mock_search_store:
        mock_search_store.return_value = mock_search
        
        # Test retrieval with duplicate suppression enabled (default)
        result = await policy_retriever.retrieve_relevant_policies(
            payer="Anthem",
            diagnosis="some condition",
            procedure="some surgery",
            suppress_duplicates=True,
            threshold=0.30
        )
        
        assert result.status == "SUCCESS"
        # Total unique text blocks should be 2 ("Identical text body content" and "Medically necessary details...")
        assert len(result.chunks) == 2
        
        chunk_texts = [chunk.text for chunk, score in result.chunks]
        assert chunk_texts.count("Identical text body content.") == 1

@pytest.mark.anyio
async def test_retrieval_metadata_filters(mock_candidates):
    mock_search = [(c, 0.60) for c in mock_candidates]

    with patch("app.services.policy_retriever.search_vector_store", new_callable=AsyncMock) as mock_search_store:
        mock_search_store.return_value = mock_search

        # 1. Test filtering by section name "Medical Necessity"
        result_sec = await policy_retriever.retrieve_relevant_policies(
            payer="Anthem",
            diagnosis="some condition",
            procedure="some procedure",
            section_filter=["Medical Necessity"],
            threshold=0.30
        )
        assert result_sec.status == "SUCCESS"
        assert len(result_sec.chunks) > 0
        for chunk, score in result_sec.chunks:
            assert chunk.section == "Medical Necessity"

        # 2. Test filtering by policy ID "CG-SURG-83"
        result_id = await policy_retriever.retrieve_relevant_policies(
            payer="Anthem",
            diagnosis="some condition",
            procedure="some procedure",
            policy_id_filter=["CG-SURG-83"],
            threshold=0.30
        )
        assert result_id.status == "SUCCESS"
        assert len(result_id.chunks) == 1
        assert result_id.chunks[0][0].policy_id == "CG-SURG-83"

@pytest.mark.anyio
async def test_retrieval_custom_threshold(mock_candidates):
    # Query returns matches with similarity 0.50
    mock_search = [(mock_candidates[2], 0.50)]

    with patch("app.services.policy_retriever.search_vector_store", new_callable=AsyncMock) as mock_search_store:
        mock_search_store.return_value = mock_search

        # 1. Custom high threshold (similarity score 0.50 is below 0.90) -> INSUFFICIENT_EVIDENCE
        result_high = await policy_retriever.retrieve_relevant_policies(
            payer="Anthem",
            diagnosis="some condition",
            procedure="some procedure",
            threshold=0.90
        )
        assert result_high.status == "INSUFFICIENT_POLICY_EVIDENCE"
        assert len(result_high.chunks) == 0

        # 2. Custom low threshold (similarity score 0.50 is above 0.20) -> SUCCESS
        result_low = await policy_retriever.retrieve_relevant_policies(
            payer="Anthem",
            diagnosis="some condition",
            procedure="some procedure",
            threshold=0.20
        )
        assert result_low.status == "SUCCESS"
        assert len(result_low.chunks) == 1
