from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

from app.schemas.users import ApprovalStatus


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    mobile: str  # changed from int to str

    model_config = ConfigDict(from_attributes=True)

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"


class AllUserResponse(UserResponse):
    model_config = ConfigDict(from_attributes=True)

    role: str
    is_active: bool
    approved: ApprovalStatus
    verified_at: Optional[datetime]
    updated_at: datetime



class ApprovedUsers(UserResponse):
    model_config = ConfigDict(from_attributes=True)

    approved: ApprovalStatus



class PendingApprovals(UserResponse):
    model_config = ConfigDict(from_attributes=True)

    approved: ApprovalStatus


class RejectedApprovals(UserResponse):
    model_config = ConfigDict(from_attributes=True)

    approved: ApprovalStatus



class AdminDashboard(BaseModel):
    approved: List[ApprovedUsers]
    pending: List[PendingApprovals]
    rejected: List[RejectedApprovals]
    approved_count: int
    pending_count: int
    rejected_count: int
    total: int


class ManufacturesInTheSystem(BaseModel):
    approved: List[ApprovedUsers]
    pending: List[PendingApprovals]

class ManufacturesForApproval(BaseModel):
    pending: List[PendingApprovals]



