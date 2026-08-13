from pydantic import BaseModel
from typing import List, Optional

class PolicyCriterion(BaseModel):
    criterion_id: str
    description: str
    required: bool
    operator: Optional[str] = None  # e.g., ">=", "<=", "==", "contains"
    required_value: Optional[float] = None
    unit: Optional[str] = None  # e.g., "weeks", "months", "years", "trials"
    source_page: int
    source_section: str

    model_config = {
        "from_attributes": True
    }

class PolicyCriteriaOutput(BaseModel):
    policy_name: str
    criteria: List[PolicyCriterion] = []

    model_config = {
        "from_attributes": True
    }
