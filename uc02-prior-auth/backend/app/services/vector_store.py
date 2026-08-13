import os
import json
import logging
import shutil
from typing import List, Tuple, Optional
import numpy as np
import faiss
from app.models.policy import PolicyChunk
from app.services.embedding_client import generate_embeddings

logger = logging.getLogger(__name__)

# Paths for storing the index and corresponding chunk metadata
INDEX_DIR = "/Users/jaikishorep/Desktop/UC02/uc02-prior-auth/backend/data/index"
ACTIVE_INDEX_PATH = os.path.join(INDEX_DIR, "index.faiss")
ACTIVE_METADATA_PATH = os.path.join(INDEX_DIR, "chunks.json")

# Temporary directories for safe rebuilds
TMP_INDEX_DIR = os.path.join(INDEX_DIR, "tmp")
TMP_INDEX_PATH = os.path.join(TMP_INDEX_DIR, "index.faiss")
TMP_METADATA_PATH = os.path.join(TMP_INDEX_DIR, "chunks.json")

# Cached active index in memory
_active_index: Optional[faiss.IndexFlatIP] = None
_active_chunks: List[PolicyChunk] = []

def get_active_vector_store() -> Tuple[Optional[faiss.IndexFlatIP], List[PolicyChunk]]:
    """Loads and caches the active vector index and chunk metadata."""
    global _active_index, _active_chunks
    
    if _active_index is not None and _active_chunks:
        return _active_index, _active_chunks

    if not os.path.exists(ACTIVE_INDEX_PATH) or not os.path.exists(ACTIVE_METADATA_PATH):
        logger.warning("Active vector store files do not exist yet. Please trigger a rebuild.")
        return None, []

    try:
        index = faiss.read_index(ACTIVE_INDEX_PATH)
        with open(ACTIVE_METADATA_PATH, "r") as f:
            meta_list = json.load(f)
            chunks = [PolicyChunk.model_validate(c) for c in meta_list]
            
        _active_index = index
        _active_chunks = chunks
        logger.info(f"Loaded active FAISS index containing {len(chunks)} vectors.")
        return _active_index, _active_chunks
    except Exception as e:
        logger.error(f"Failed to load active FAISS index: {e}")
        return None, []

def clear_cache():
    """Clears in-memory active index cache (for testing/rebuilding)."""
    global _active_index, _active_chunks
    _active_index = None
    _active_chunks = []

async def rebuild_vector_index(chunks: List[PolicyChunk]) -> bool:
    """
    Builds the vector index to a temporary directory, validates it, and promotes it to active.
    Ensures that a failed rebuild does not destroy the last good index.
    """
    if not chunks:
        logger.warning("No chunks provided to build vector index.")
        return False

    os.makedirs(TMP_INDEX_DIR, exist_ok=True)
    logger.info(f"Rebuilding vector index for {len(chunks)} chunks...")

    # 1. Generate embeddings in batches to prevent rate limit limits
    texts = [c.text for c in chunks]
    batch_size = 50
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i : i + batch_size]
        try:
            embeddings = await generate_embeddings(batch_texts)
            all_embeddings.extend(embeddings)
        except Exception as e:
            logger.error(f"Failed to generate embeddings for batch {i//batch_size + 1}: {e}")
            raise e

    if len(all_embeddings) != len(chunks):
        raise ValueError(
            f"Embedding length mismatch: generated {len(all_embeddings)} embeddings for {len(chunks)} chunks."
        )

    # 2. Setup FAISS Index
    vectors = np.array(all_embeddings, dtype=np.float32)
    
    # Normalize vectors for Inner Product (Cosine Similarity) search
    faiss.normalize_L2(vectors)
    
    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    # 3. Save to temporary files
    faiss.write_index(index, TMP_INDEX_PATH)
    
    serialized_chunks = [c.model_dump() for c in chunks]
    with open(TMP_METADATA_PATH, "w") as f:
        json.dump(serialized_chunks, f, indent=2)

    # 4. Validate temporary files
    if not validate_index_store(TMP_INDEX_PATH, TMP_METADATA_PATH):
        logger.error("Validation failed for the built temporary index. Aborting promotion.")
        return False

    # 5. Safe promotion: Replace active index files
    os.makedirs(INDEX_DIR, exist_ok=True)
    
    # Move tmp/index.faiss -> index.faiss
    if os.path.exists(ACTIVE_INDEX_PATH):
        os.remove(ACTIVE_INDEX_PATH)
    shutil.move(TMP_INDEX_PATH, ACTIVE_INDEX_PATH)

    # Move tmp/chunks.json -> chunks.json
    if os.path.exists(ACTIVE_METADATA_PATH):
        os.remove(ACTIVE_METADATA_PATH)
    shutil.move(TMP_METADATA_PATH, ACTIVE_METADATA_PATH)

    # Clean tmp folder
    if os.path.exists(TMP_INDEX_DIR):
        shutil.rmtree(TMP_INDEX_DIR)

    # Clear memory cache
    clear_cache()
    logger.info("Successfully promoted new FAISS vector store index to active status.")
    return True

def validate_index_store(index_path: str, metadata_path: str) -> bool:
    """Performs validation checks to ensure index and metadata sizes map correctly."""
    if not os.path.exists(index_path) or not os.path.exists(metadata_path):
        return False
    try:
        index = faiss.read_index(index_path)
        with open(metadata_path, "r") as f:
            chunks = json.load(f)
        
        # Verify sizes match
        if index.ntotal != len(chunks):
            logger.error(f"Size mismatch: FAISS index has {index.ntotal} vectors but chunks metadata has {len(chunks)} elements.")
            return False
            
        # Verify dimensions match standard openai embeddings (1536)
        if index.d != 1536:
            logger.error(f"Dimension mismatch: expected 1536 but index has {index.d}.")
            return False
            
        return True
    except Exception as e:
        logger.error(f"Failed to validate index files: {e}")
        return False

async def search_vector_store(query_text: str, k: int = 5) -> List[Tuple[PolicyChunk, float]]:
    """
    Queries the active FAISS index using cosine similarity (L2-normalized inner product).
    Returns list of matched (PolicyChunk, similarity_score) tuples.
    """
    index, chunks = get_active_vector_store()
    if index is None or not chunks:
        logger.warning("Active vector store index is empty or not loaded.")
        return []

    # 1. Embed query
    query_embeddings = await generate_embeddings([query_text])
    if not query_embeddings:
        return []

    query_vector = np.array(query_embeddings, dtype=np.float32)
    faiss.normalize_L2(query_vector)

    # 2. Run search
    scores, indices = index.search(query_vector, k)

    # 3. Compile results
    results = []
    # index.search returns a 2D array of results for each query in batch
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(chunks):
            continue
        results.append((chunks[idx], float(score)))

    return results
