from pydantic import BaseModel
from typing import Optional



class VerificationCreate(BaseModel):
    drug_id: int
    location: str
    device_info: str
    user_id: Optional[int] = None
    is_authentic: Optional[bool] = True

class VerificationUpdate(BaseModel):
    location: Optional[str] = None
    device_info: Optional[str] = None
    user_id: Optional[int] = None
    is_authentic: Optional[bool] = None





