import random
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.authorization import AuthorizationCreate, AuthorizationResponse
from app.database.mongodb import get_database

router = APIRouter(prefix="/api/authorizations", tags=["authorizations"])

# Initial mock data for pre-populating empty database
INITIAL_DOCS = [
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

def format_doc(doc) -> dict:
    if not doc:
        return doc
    doc_copy = dict(doc)
    if "_id" in doc_copy:
        doc_copy["_id"] = str(doc_copy["_id"])
    return doc_copy

async def ensure_initial_data(db: AsyncIOMotorDatabase):
    count = await db.prior_authorizations.count_documents({})
    if count == 0:
        await db.prior_authorizations.insert_many(INITIAL_DOCS)

@router.post("", response_model=AuthorizationResponse, status_code=status.HTTP_201_CREATED)
async def create_authorization(payload: AuthorizationCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    # Generate unique ID
    new_id = f"PA-{random.randint(1000, 9999)}"
    
    # Ensure ID uniqueness in database
    while await db.prior_authorizations.find_one({"id": new_id}) is not None:
        new_id = f"PA-{random.randint(1000, 9999)}"

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

    await db.prior_authorizations.insert_one(new_auth)
    return format_doc(new_auth)

@router.get("", response_model=List[AuthorizationResponse])
async def list_authorizations(db: AsyncIOMotorDatabase = Depends(get_database)):
    await ensure_initial_data(db)
    cursor = db.prior_authorizations.find().sort("created_at", -1)
    auths = await cursor.to_list(length=100)
    return [format_doc(auth) for auth in auths]

@router.get("/{authorization_id}", response_model=AuthorizationResponse)
async def get_authorization(authorization_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    auth = await db.prior_authorizations.find_one({"id": authorization_id})
    if auth:
        return format_doc(auth)
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Authorization request with ID '{authorization_id}' not found"
    )
