from pydantic import BaseModel
from datetime import date
from typing import Optional


class BatchBase(BaseModel):
    batch_number: str
    manufacturer_id: int
    manufacturing_date: date
    expiry_date: date
    status: str  # Could be 'active', 'recalled', 'expired'

class BatchCreate(BatchBase):
    pass

class BatchUpdate(BaseModel):
    manufacturing_date: Optional[date] = None
    expiry_date: Optional[date] = None
    status: Optional[str] = None
