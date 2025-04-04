from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class DrugBase(BaseModel):
    serial_number: str
    batch_id: int
    name: str
    dosage: str
    description: Optional[str] = None
    qr_code: str
    is_verified: Optional[bool] = False


class DrugResponse(DrugBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


