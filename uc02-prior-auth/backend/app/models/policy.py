from pydantic import BaseModel
from typing import Optional

class ParsedPage(BaseModel):
    payer: str
    policy_name: str
    policy_id: Optional[str] = None
    effective_date: Optional[str] = None
    source_file: str
    page_number: int  # 1-indexed
    text: str
    scanned: bool = False

    model_config = {
        "from_attributes": True
    }
