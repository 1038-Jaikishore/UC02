import os
import shutil
import pytest
from unittest.mock import AsyncMock, patch
from app.models.policy import PolicyChunk
from app.services import vector_store

TEST_INDEX_DIR = "/Users/jaikishorep/Desktop/UC02/uc02-prior-auth/backend/data/index"

@pytest.fixture(autouse=True)
def clean_test_index_dir():
    # Make sure we clean up test index files before and after each test
    vector_store.clear_cache()
    if os.path.exists(TEST_INDEX_DIR):
        # Delete only files inside, or the folder itself
        shutil.rmtree(TEST_INDEX_DIR)
    yield
    vector_store.clear_cache()
    if os.path.exists(TEST_INDEX_DIR):
        shutil.rmtree(TEST_INDEX_DIR)

@pytest.mark.anyio
async def test_rebuild_and_search_vector_store_success():
    # Create mock chunks
    chunks = [
        PolicyChunk(
            source_type="PAYER",
            source_name="Anthem",
            policy_name="Obesity Policy",
            policy_id="CG-SURG-83",
            effective_date="Nov 2025",
            source_file="severe_obesity.pdf",
            page_number=1,
            section="Description",
            text="This is Anthem bariatric surgery coverage guidelines.",
            chunk_index=0
        ),
        PolicyChunk(
            source_type="PAYER",
            source_name="Uhc",
            policy_name="Sleep Study Policy",
            policy_id="MP.001",
            effective_date="July 2026",
            source_file="sleep_studies.pdf",
            page_number=2,
            section="Medical Necessity",
            text="UHC sleep studies are medically necessary for sleep apnea diagnosis.",
            chunk_index=1
        )
    ]

    # Mock embeddings generation (returns dummy 1536-dim unit vectors)
    mock_emb_1 = [1.0] + [0.0] * 1535
    mock_emb_2 = [0.0, 1.0] + [0.0] * 1534
    dummy_embeddings = [mock_emb_1, mock_emb_2]

    with patch("app.services.vector_store.generate_embeddings", new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = dummy_embeddings
        
        # Build index
        success = await vector_store.rebuild_vector_index(chunks)
        assert success is True
        
        # Verify files are promoted to active
        assert os.path.exists(vector_store.ACTIVE_INDEX_PATH)
        assert os.path.exists(vector_store.ACTIVE_METADATA_PATH)

    # Verify query works using mocked query embedding (closer to mock_emb_1)
    with patch("app.services.vector_store.generate_embeddings", new_callable=AsyncMock) as mock_query_generate:
        # Mock search query embedding
        mock_query_generate.return_value = [[1.0] + [0.0] * 1535]
        
        results = await vector_store.search_vector_store("bariatric surgery", k=2)
        
        assert len(results) == 2
        matched_chunk, similarity = results[0]
        assert isinstance(matched_chunk, PolicyChunk)
        assert matched_chunk.policy_name == "Obesity Policy"
        assert similarity > 0.0

@pytest.mark.anyio
async def test_rebuild_index_failure_preserves_old_index():
    # 1. First build a valid initial index
    chunks = [
        PolicyChunk(
            source_type="PAYER",
            source_name="Anthem",
            policy_name="Obesity Policy",
            source_file="severe_obesity.pdf",
            page_number=1,
            section="Description",
            text="First index content.",
            chunk_index=0
        )
    ]
    
    with patch("app.services.vector_store.generate_embeddings", new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = [[0.05] * 1536]
        success = await vector_store.rebuild_vector_index(chunks)
        assert success is True
        
    # Get active store and verify loaded
    idx, loaded_chunks = vector_store.get_active_vector_store()
    assert len(loaded_chunks) == 1
    assert loaded_chunks[0].text == "First index content."

    # 2. Rebuild fails due to API exception
    with patch("app.services.vector_store.generate_embeddings", new_callable=AsyncMock) as mock_generate_fail:
        mock_generate_fail.side_effect = RuntimeError("OpenRouter credit outage!")
        
        with pytest.raises(RuntimeError):
            await vector_store.rebuild_vector_index(chunks)

    # 3. Verify original index was NOT corrupted or lost and is still active
    vector_store.clear_cache()
    idx2, loaded_chunks2 = vector_store.get_active_vector_store()
    assert len(loaded_chunks2) == 1
    assert loaded_chunks2[0].text == "First index content."
