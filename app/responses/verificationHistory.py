from datetime import datetime
from pydantic import BaseModel
from typing import Optional



class VerificationBase(BaseModel):
    drug_id: int
    location: str
    device_info: str
    user_id: Optional[int] = None
    is_authentic: Optional[bool] = True


class VerificationResponse(VerificationBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

