from pydantic import BaseModel
from typing import Optional

class DrugCreate(BaseModel):
    serial_number: str
    batch_id: int
    name: str
    dosage: str
    description: Optional[str] = None
    qr_code: str
    is_verified: Optional[bool] = False


class DrugUpdate(BaseModel):
    batch_id: int
    name: Optional[str] = None
    dosage: Optional[str] = None
    description: Optional[str] = None
    is_verified: Optional[bool] = None

