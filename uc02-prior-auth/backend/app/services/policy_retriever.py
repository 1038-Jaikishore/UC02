import logging
from typing import List, Tuple, Optional
from pydantic import BaseModel
from app.models.policy import PolicyChunk
from app.services.vector_store import search_vector_store

logger = logging.getLogger(__name__)

# Minimum similarity score threshold for successful retrieval
SIMILARITY_THRESHOLD = 0.35

class RetrievalResult(BaseModel):
    status: str  # SUCCESS, PAYER_UNKNOWN, INSUFFICIENT_POLICY_EVIDENCE
    chunks: List[Tuple[PolicyChunk, float]] = []

async def retrieve_relevant_policies(
    payer: Optional[str],
    diagnosis: str,
    procedure: str,
    cpt_code: Optional[str] = None,
    hcpcs_code: Optional[str] = None,
    clinical_context: Optional[str] = "",
    k: int = 5
) -> RetrievalResult:
    """
    Retrieves and ranks relevant medical policy chunks for a given request.
    Enforces payer isolation, structured CPT/HCPCS boosting, and similarity thresholds.
    """
    # 1. Enforce Unknown Payer Check
    if not payer or payer.strip().lower() not in ["anthem", "uhc"]:
        logger.warning(f"Unknown or unsupported payer: {payer}")
        return RetrievalResult(status="PAYER_UNKNOWN", chunks=[])

    # 2. Formulate query string
    # E.g. "Lumbar MRI medical necessity coverage criteria chronic lower back pain CPT 72148"
    query_parts = [procedure, "medical necessity coverage criteria", diagnosis]
    if cpt_code:
        query_parts.append(f"CPT {cpt_code}")
    if hcpcs_code:
        query_parts.append(f"HCPCS {hcpcs_code}")
    if clinical_context:
        query_parts.append(clinical_context)

    query_text = " ".join(query_parts).strip()
    logger.info(f"RAG Retrieval Query for payer '{payer}': {query_text}")

    # Retrieve candidate chunks (fetch more to allow payer filtering & code boosting)
    raw_results = await search_vector_store(query_text, k=30)
    if not raw_results:
        return RetrievalResult(status="INSUFFICIENT_POLICY_EVIDENCE", chunks=[])

    # 3. Payer Isolation Filter
    # Only keep chunks belonging strictly to the requested payer
    payer_filtered = []
    for chunk, score in raw_results:
        if chunk.source_name.lower() == payer.strip().lower():
            payer_filtered.append((chunk, score))

    if not payer_filtered:
        logger.warning(f"No policy chunks found matching payer '{payer}'.")
        return RetrievalResult(status="INSUFFICIENT_POLICY_EVIDENCE", chunks=[])

    # 4. Structured Code Boosting & Ranking
    # Boost chunks that explicitly list the CPT or HCPCS code in their metadata or text
    boosted_results = []
    for chunk, score in payer_filtered:
        boost = 0.0
        
        # Check metadata list
        has_cpt_meta = cpt_code and (cpt_code in chunk.cpt_codes)
        has_hcpcs_meta = hcpcs_code and (hcpcs_code in chunk.hcpcs_codes)
        
        # Check text body as fallback
        has_cpt_text = cpt_code and (cpt_code in chunk.text)
        has_hcpcs_text = hcpcs_code and (hcpcs_code in chunk.text)

        if has_cpt_meta or has_hcpcs_meta:
            boost += 0.30  # High boost for exact metadata matching
        elif has_cpt_text or has_hcpcs_text:
            boost += 0.15  # Medium boost for mention in text body
            
        final_score = score + boost
        boosted_results.append((chunk, final_score))

    # Sort candidates by boosted score descending
    boosted_results.sort(key=lambda x: x[1], reverse=True)

    # 5. Threshold validation
    highest_score = boosted_results[0][1]
    if highest_score < SIMILARITY_THRESHOLD:
        logger.warning(f"Top matched chunk score ({highest_score:.3f}) is below threshold ({SIMILARITY_THRESHOLD}).")
        return RetrievalResult(status="INSUFFICIENT_POLICY_EVIDENCE", chunks=[])

    # Return top k results
    return RetrievalResult(
        status="SUCCESS",
        chunks=boosted_results[:k]
    )
