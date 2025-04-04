from pydantic import BaseModel, EmailStr
from typing import Optional

class ManufacturerCreate(BaseModel):
    name: str
    license_number: str
    address: str
    contact_email: EmailStr
    contact_phone: str
    user_id: Optional[int] = None
    license_file: Optional[str] = None
    certificate_file: Optional[str] = None



class ManufacturerUpdate(BaseModel):
    name: Optional[str] = None
    license_number: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    user_id: Optional[int] = None
    license_file: Optional[str] = None
    certificate_file: Optional[str] = None

