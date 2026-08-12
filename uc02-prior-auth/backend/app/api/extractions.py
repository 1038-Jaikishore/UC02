import os
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database.mongodb import get_database
from app.services import clinical_extractor
from app.models.extraction import ClinicalExtractionRecord

router = APIRouter(prefix="/api/authorizations", tags=["extractions"])

def format_doc(doc) -> dict:
    if not doc:
        return doc
    doc_copy = dict(doc)
    if "_id" in doc_copy:
        doc_copy["_id"] = str(doc_copy["_id"])
    return doc_copy

@router.get("/{authorization_id}/extraction", response_model=ClinicalExtractionRecord)
async def get_clinical_extraction(
    authorization_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Retrieves the clinical extraction record for a given authorization request.
    If it does not exist, triggers extraction dynamically, saves it, and returns it.
    """
    # 1. Check if extraction is already cached
    record = await db.clinical_extractions.find_one({"authorization_id": authorization_id})
    if record:
        return format_doc(record)
        
    # 2. If not found, load the authorization request
    auth = await db.prior_authorizations.find_one({"id": authorization_id})
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Authorization request with ID '{authorization_id}' not found"
        )
        
    # 3. Perform extraction dynamically
    try:
        clinical_notes = auth.get("clinical_notes", "")
        patient_id = auth.get("patient_id")
        
        extracted_data = await clinical_extractor.extract_clinical_info(clinical_notes)
        
        new_record = {
            "authorization_id": authorization_id,
            "patient_id": patient_id,
            "structured_extraction": extracted_data.model_dump(),
            "model": os.getenv("LLM_MODEL", "google/gemini-2.5-flash"),
            "timestamp": datetime.now(timezone.utc),
            "extraction_version": "1.0.0",
            "validation_status": "VALID"
        }
        
        await db.clinical_extractions.replace_one(
            {"authorization_id": authorization_id},
            new_record,
            upsert=True
        )
        
        return format_doc(new_record)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Clinical fact extraction failed: {str(e)}"
        )

@router.post("/{authorization_id}/extraction", response_model=ClinicalExtractionRecord)
async def trigger_clinical_extraction(
    authorization_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Forces a fresh run of the clinical extractor for the given authorization request,
    overwriting any previously saved extraction.
    """
    auth = await db.prior_authorizations.find_one({"id": authorization_id})
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Authorization request with ID '{authorization_id}' not found"
        )
        
    try:
        clinical_notes = auth.get("clinical_notes", "")
        patient_id = auth.get("patient_id")
        
        extracted_data = await clinical_extractor.extract_clinical_info(clinical_notes)
        
        new_record = {
            "authorization_id": authorization_id,
            "patient_id": patient_id,
            "structured_extraction": extracted_data.model_dump(),
            "model": os.getenv("LLM_MODEL", "google/gemini-2.5-flash"),
            "timestamp": datetime.now(timezone.utc),
            "extraction_version": "1.0.0",
            "validation_status": "VALID"
        }
        
        await db.clinical_extractions.replace_one(
            {"authorization_id": authorization_id},
            new_record,
            upsert=True
        )
        
        return format_doc(new_record)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Clinical fact extraction failed: {str(e)}"
        )
