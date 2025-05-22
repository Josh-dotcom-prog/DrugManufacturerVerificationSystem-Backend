from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    mobile: int

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"

class AllUserResponse(UserResponse):
    role: str
    is_active: bool
    approved: bool
    verified_at: Optional[datetime]
    updated_at: datetime


class ApprovedUsers(UserResponse):
    approved: bool = True

class PendingApprovals(UserResponse):
    approved: bool = False

class AdminDashboard(UserResponse):
    approved: List[ApprovedUsers]
    pending: List[PendingApprovals]
    approved_count: int
    pending_count: int
    total: int

