from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ClinicalExtraction(BaseModel):
    diagnosis: Optional[str] = Field(None, description="The primary diagnosed condition.")
    requested_procedure: Optional[str] = Field(None, description="The name of the requested prior auth procedure.")
    symptom_duration_weeks: Optional[int] = Field(None, description="The duration of patient symptoms in weeks. Null if unspecified.")
    physiotherapy_weeks: Optional[int] = Field(None, description="The duration of physiotherapy completed in weeks. Null if unspecified.")
    medications_attempted: List[str] = Field(default_factory=list, description="List of anti-inflammatory, steroid, or other relevant medications tried.")
    previous_imaging: List[str] = Field(default_factory=list, description="Historical scans or imaging (e.g. X-Ray, MRI, CT) received.")
    relevant_conditions: List[str] = Field(default_factory=list, description="Other historical/chronic conditions or risk factors.")
    unknown_fields: List[str] = Field(default_factory=list, description="List of clinical concepts or metrics that are completely missing/unspecified in the notes.")

class ClinicalExtractionRecord(BaseModel):
    authorization_id: str
    patient_id: str
    structured_extraction: ClinicalExtraction
    model: str
    timestamp: datetime
    extraction_version: str = "1.0.0"
    validation_status: str = "VALID"

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }
