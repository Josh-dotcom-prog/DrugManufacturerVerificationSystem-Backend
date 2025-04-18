from pydantic import BaseModel
from datetime import date
from typing import Optional
import enum


class BatchStatus(str, enum.Enum):
    active = "active"
    recalled = "recalled"
    expired = "expired"

class BatchCreate(BaseModel):
    batch_number: str
    manufacturer_id: int
    manufacturing_date: date
    expiry_date: date
    status: BatchStatus  # Could be 'active', 'recalled', 'expired'


class BatchUpdate(BaseModel):
    batch_number: str
    manufacturing_date: Optional[date] = None
    expiry_date: Optional[date] = None
    status: Optional[BatchStatus]
