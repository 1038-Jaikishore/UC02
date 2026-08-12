from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Demographics(BaseModel):
    patient_id: str
    first_name: str
    last_name: str
    dob: str
    age: int
    gender: str
    insurance_plan: str
    member_id: str
    summary_card_text: str

class PatientProfileResponse(BaseModel):
    patient_id: str
    demographics: Demographics
    conditions: List[dict] = []
    medications: List[dict] = []
    procedures: List[dict] = []
    diagnostic_results: List[dict] = []
    vital_signs: List[dict] = []
    encounters: List[dict] = []
    clinical_assessments: List[dict] = []
    functional_status: List[dict] = []
    allergies: List[dict] = []
    surgeries: List[dict] = []
    medical_equipment: List[dict] = []
    referrals: List[dict] = []
    family_history: List[dict] = []
    social_history: List[dict] = []
    immunizations: List[dict] = []

    model_config = {
        "from_attributes": True
    }

class PatientSummaryResponse(BaseModel):
    patient_id: str
    first_name: str
    last_name: str
    age: int
    gender: str
    insurance_plan: str
    member_id: str

    model_config = {
        "from_attributes": True
    }
