import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.models.authorization import AuthorizationCreate, AuthorizationResponse

router = APIRouter(prefix="/api/authorizations", tags=["authorizations"])

# In-memory mock database matching Phase 1 initial list
DB_AUTHORIZATIONS = [
    {
        "id": "PA-4011",
        "patient_id": "PT-5510",
        "diagnosis": "Severe primary osteoarthritis of right knee",
        "diagnosis_code": "M17.11",
        "requested_procedure": "Total knee arthroplasty, right",
        "cpt_code": "27447",
        "clinical_notes": "Patient is a 68-year-old female with severe right knee pain for >12 months. Unable to walk >1 block. Conservative treatments failed including physical therapy (12 weeks) and NSAIDs. X-rays reveal bone-on-bone joint space narrowing.",
        "priority": "Standard",
        "status": "PENDING_REVIEW",
        "created_at": "2026-08-10",
        "supporting_documents": ["xray_right_knee.pdf", "clinical_summary_PT-5510.pdf"]
    },
    {
        "id": "PA-4012",
        "patient_id": "PT-7721",
        "diagnosis": "Spinal stenosis, lumbar region",
        "diagnosis_code": "M48.061",
        "requested_procedure": "Decompression laminectomy, lumbar, single segment",
        "cpt_code": "63047",
        "clinical_notes": "Patient reports progressive bilateral leg pain and numbness aggravated by walking. MRI reveals severe central canal stenosis at L4-L5. Symptoms unresponsive to epidural steroid injections.",
        "priority": "Urgent",
        "status": "PENDING_REVIEW",
        "created_at": "2026-08-11",
        "supporting_documents": ["mri_lumbar_spine.pdf"]
    },
    {
        "id": "PA-4013",
        "patient_id": "PT-2294",
        "diagnosis": "Degenerative meniscus tear, medial",
        "diagnosis_code": "S83.242A",
        "requested_procedure": "Arthroscopic partial meniscectomy, medial",
        "cpt_code": "29881",
        "clinical_notes": "Patient reports persistent mechanical catching and locking in the medial knee compartment for 6 months. Failed conservative management.",
        "priority": "Standard",
        "status": "APPROVED",
        "created_at": "2026-08-08",
        "supporting_documents": ["mri_medial_meniscus.pdf"]
    }
]

@router.post("", response_model=AuthorizationResponse, status_code=status.HTTP_201_CREATED)
async def create_authorization(payload: AuthorizationCreate):
    # Generate unique ID (e.g. PA-XXXX)
    import random
    new_id = f"PA-{random.randint(1000, 9999)}"
    
    # Ensure ID uniqueness in memory
    while any(auth["id"] == new_id for auth in DB_AUTHORIZATIONS):
        new_id = f"PA-{random.randint(1000, 9999)}"

    from datetime import timezone
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    new_auth = {
        "id": new_id,
        "patient_id": payload.patient_id,
        "diagnosis": payload.diagnosis,
        "diagnosis_code": payload.diagnosis_code,
        "requested_procedure": payload.requested_procedure,
        "cpt_code": payload.cpt_code,
        "clinical_notes": payload.clinical_notes,
        "priority": payload.priority,
        "status": "PENDING_REVIEW",
        "created_at": today_str,
        "supporting_documents": ["uploaded_clinical_summary.pdf"]
    }

    DB_AUTHORIZATIONS.insert(0, new_auth)
    return new_auth

@router.get("", response_model=List[AuthorizationResponse])
async def list_authorizations():
    return DB_AUTHORIZATIONS

@router.get("/{authorization_id}", response_model=AuthorizationResponse)
async def get_authorization(authorization_id: str):
    for auth in DB_AUTHORIZATIONS:
        if auth["id"] == authorization_id:
            return auth
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Authorization request with ID '{authorization_id}' not found"
    )
