from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class AuthorizationCreate(BaseModel):
    patient_id: str = Field(..., min_length=1, description="Unique identifier for the patient")
    diagnosis: str = Field(..., min_length=1, description="Clinical diagnosis description")
    diagnosis_code: str = Field(..., min_length=1, description="ICD-10 diagnosis code")
    requested_procedure: str = Field(..., min_length=1, description="Name of the procedure requested")
    cpt_code: str = Field(..., min_length=1, description="CPT procedure code")
    clinical_notes: str = Field(..., min_length=1, description="Detailed clinical notes / justification")
    priority: str = Field("Standard", description="Priority level (Standard or Urgent)")

class AuthorizationResponse(BaseModel):
    id: str
    patient_id: str
    diagnosis: str
    diagnosis_code: str
    requested_procedure: str
    cpt_code: str
    clinical_notes: str
    priority: str
    status: str
    created_at: str
    supporting_documents: List[str]

    model_config = {
        "from_attributes": True
    }
