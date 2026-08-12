import re
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database.mongodb import get_database
from app.models.patient import PatientProfileResponse, PatientSummaryResponse

router = APIRouter(prefix="/api/patients", tags=["patients"])

def format_doc(doc) -> dict:
    if not doc:
        return doc
    doc_copy = dict(doc)
    if "_id" in doc_copy:
        doc_copy["_id"] = str(doc_copy["_id"])
    return doc_copy

@router.get("", response_model=List[PatientSummaryResponse])
async def list_patients(
    search: Optional[str] = Query(None, description="Search by Patient ID, First Name, or Last Name"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    query = {}
    if search:
        # Regex search for first name, last name, or patient ID (case-insensitive)
        search_regex = {"$regex": re.escape(search), "$options": "i"}
        query = {
            "$or": [
                {"patient_id": search_regex},
                {"demographics.first_name": search_regex},
                {"demographics.last_name": search_regex}
            ]
        }

    cursor = db.patients.find(query).sort("patient_id", 1)
    patients = await cursor.to_list(length=100)
    
    # Map to summary response structure
    summaries = []
    for p in patients:
        demo = p.get("demographics", {})
        summaries.append({
            "patient_id": p["patient_id"],
            "first_name": demo.get("first_name", ""),
            "last_name": demo.get("last_name", ""),
            "age": demo.get("age", 0),
            "gender": demo.get("gender", ""),
            "insurance_plan": demo.get("insurance_plan", ""),
            "member_id": demo.get("member_id", "")
        })
        
    return summaries

@router.get("/{patient_id}", response_model=PatientProfileResponse)
async def get_patient_profile(
    patient_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    patient = await db.patients.find_one({"patient_id": patient_id})
    if patient:
        return format_doc(patient)
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Patient profile with ID '{patient_id}' not found"
    )
