from pydantic import BaseModel
from typing import Optional, List

class ParsedPage(BaseModel):
    payer: str
    policy_name: str
    policy_id: Optional[str] = None
    effective_date: Optional[str] = None
    source_file: str
    page_number: int  # 1-indexed
    text: str
    scanned: bool = False
    cpt_codes: List[str] = []
    hcpcs_codes: List[str] = []

    model_config = {
        "from_attributes": True
    }

class PolicyChunk(BaseModel):
    source_type: str = "PAYER"
    source_name: str  # Anthem or UHC
    policy_name: str
    policy_id: Optional[str] = None
    effective_date: Optional[str] = None
    source_file: str
    page_number: int
    section: str
    text: str
    chunk_index: int
    cpt_codes: List[str] = []
    hcpcs_codes: List[str] = []

    model_config = {
        "from_attributes": True
    }
