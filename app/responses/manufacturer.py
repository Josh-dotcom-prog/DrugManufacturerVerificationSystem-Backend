from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class ManufacturerBase(BaseModel):
    name: str
    license_number: str
    address: str
    contact_email: EmailStr
    contact_phone: str
    user_id: Optional[int] = None
    license_file: Optional[str] = None
    certificate_file: Optional[str] = None

class ManufacturerResponse(ManufacturerBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


