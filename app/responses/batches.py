from pydantic import BaseModel
from datetime import date
from typing import Optional
from datetime import datetime


class BatchBase(BaseModel):
    batch_number: str
    manufacturer_id: int
    manufacturing_date: date
    expiry_date: date
    status: str  # Could be 'active', 'recalled', 'expired'

class BatchResponse(BatchBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


