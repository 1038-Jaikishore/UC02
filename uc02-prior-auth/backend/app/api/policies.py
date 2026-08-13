from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Any
from app.services.policy_retriever import retrieve_relevant_policies
from app.services.criteria_extractor import extract_policy_criteria
from app.models.policy import PolicyChunk
from app.models.criteria import PolicyCriterion

router = APIRouter(prefix="/api/policies", tags=["policies"])

class PolicyRetrievalRequest(BaseModel):
    diagnosis: str
    requested_procedure: str
    cpt_code: Optional[str] = None
    payer: Optional[str] = None
    clinical_context: Optional[str] = ""
    mock: bool = False

class PolicyRetrievalResponse(BaseModel):
    status: str  # SUCCESS, PAYER_UNKNOWN, INSUFFICIENT_POLICY_EVIDENCE
    policy_name: str
    criteria: List[PolicyCriterion] = []
    chunks: List[PolicyChunk] = []

# Mock data mapping helper
def get_mock_response(req: PolicyRetrievalRequest) -> PolicyRetrievalResponse:
    # 1. Payer check
    payer_val = req.payer or ""
    if payer_val.strip().lower() not in ["anthem", "uhc"]:
        return PolicyRetrievalResponse(
            status="PAYER_UNKNOWN",
            policy_name="Unknown Policy",
            criteria=[],
            chunks=[]
        )

    # 2. Check procedure or code to match mock policies
    is_mri = "mri" in req.requested_procedure.lower() or req.cpt_code == "72148"
    is_wrist = "wrist" in req.requested_procedure.lower() or req.cpt_code == "25441"
    
    if payer_val.strip().lower() == "anthem" and is_mri:
        chunk = PolicyChunk(
            source_type="PAYER",
            source_name="Anthem",
            policy_name="Lumbar MRI Policy",
            source_file="lumbar_mri.pdf",
            page_number=6,
            section="Medical Necessity",
            text="Conservative therapy attempted for at least 6 weeks is required.",
            chunk_index=0,
            cpt_codes=["72148"],
            hcpcs_codes=[]
        )
        criterion = PolicyCriterion(
            criterion_id="C1",
            description="Conservative therapy attempted for at least 6 weeks",
            required=True,
            operator=">=",
            required_value=6.0,
            unit="weeks",
            source_page=6,
            source_section="Medical Necessity"
        )
        return PolicyRetrievalResponse(
            status="SUCCESS",
            policy_name="Lumbar MRI Policy",
            criteria=[criterion],
            chunks=[chunk]
        )
    elif payer_val.strip().lower() == "uhc" and is_wrist:
        chunk = PolicyChunk(
            source_type="PAYER",
            source_name="Uhc",
            policy_name="Wrist Surgery Policy",
            source_file="wrist_surgery.pdf",
            page_number=2,
            section="Medical Necessity",
            text="Medically necessary wrist repair requires documented thumb stability issues.",
            chunk_index=1,
            cpt_codes=["25441"],
            hcpcs_codes=[]
        )
        criterion = PolicyCriterion(
            criterion_id="C1",
            description="Documented thumb stability issues",
            required=True,
            operator="==",
            required_value=None,
            unit=None,
            source_page=2,
            source_section="Medical Necessity"
        )
        return PolicyRetrievalResponse(
            status="SUCCESS",
            policy_name="Wrist Surgery Policy",
            criteria=[criterion],
            chunks=[chunk]
        )
    else:
        return PolicyRetrievalResponse(
            status="INSUFFICIENT_POLICY_EVIDENCE",
            policy_name="Unknown Policy",
            criteria=[],
            chunks=[]
        )

@router.post("/retrieval", response_model=PolicyRetrievalResponse)
async def post_policy_retrieval(req: PolicyRetrievalRequest):
    """
    Performs policy chunks retrieval and extracts structured necessity criteria.
    Supports either live semantic vector query searches or mock mode responses.
    """
    # 1. Handle mock mode
    if req.mock:
        return get_mock_response(req)

    # 2. Live mode: Retrieve candidate chunks
    retrieval_res = await retrieve_relevant_policies(
        payer=req.payer,
        diagnosis=req.diagnosis,
        procedure=req.requested_procedure,
        cpt_code=req.cpt_code,
        clinical_context=req.clinical_context
    )

    if retrieval_res.status != "SUCCESS":
        return PolicyRetrievalResponse(
            status=retrieval_res.status,
            policy_name="Unknown Policy",
            criteria=[],
            chunks=[]
        )

    # 3. Extract criteria from retrieved chunks
    try:
        extracted = await extract_policy_criteria(retrieval_res.chunks)
        # Convert tuples (PolicyChunk, score) to list of PolicyChunk
        chunks_list = [chunk for chunk, score in retrieval_res.chunks]
        
        return PolicyRetrievalResponse(
            status="SUCCESS",
            policy_name=extracted.policy_name,
            criteria=extracted.criteria,
            chunks=chunks_list
        )
    except Exception as e:
        # Fall back if LLM criteria extraction fails
        return PolicyRetrievalResponse(
            status="INSUFFICIENT_POLICY_EVIDENCE",
            policy_name="Unknown Policy",
            criteria=[],
            chunks=[chunk for chunk, score in retrieval_res.chunks]
        )
