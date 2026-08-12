from pydantic import BaseModel, Field
from typing import List, Optional

class ClinicalExtraction(BaseModel):
    diagnosis: Optional[str] = Field(None, description="The primary diagnosed condition.")
    requested_procedure: Optional[str] = Field(None, description="The name of the requested prior auth procedure.")
    symptom_duration_weeks: Optional[int] = Field(None, description="The duration of patient symptoms in weeks. Null if unspecified.")
    physiotherapy_weeks: Optional[int] = Field(None, description="The duration of physiotherapy completed in weeks. Null if unspecified.")
    medications_attempted: List[str] = Field(default_factory=list, description="List of anti-inflammatory, steroid, or other relevant medications tried.")
    previous_imaging: List[str] = Field(default_factory=list, description="Historical scans or imaging (e.g. X-Ray, MRI, CT) received.")
    relevant_conditions: List[str] = Field(default_factory=list, description="Other historical/chronic conditions or risk factors.")
    unknown_fields: List[str] = Field(default_factory=list, description="List of clinical concepts or metrics that are completely missing/unspecified in the notes.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "diagnosis": "Chronic lower back pain",
                "requested_procedure": "Lumbar MRI",
                "symptom_duration_weeks": 8,
                "physiotherapy_weeks": 3,
                "medications_attempted": ["Ibuprofen"],
                "previous_imaging": ["Lumbar X-Ray"],
                "relevant_conditions": ["Osteoarthritis"],
                "unknown_fields": ["Epidural injections", "Spinal surgery history"]
            }
        }
    }
