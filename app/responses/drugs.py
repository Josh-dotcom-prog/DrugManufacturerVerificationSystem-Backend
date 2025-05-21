import enum
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from app.schemas.drugs import Category, DosageForm


class DrugBase(BaseModel):
    name: str
    category: Category
    dosage_form: DosageForm
    manufacturer: str
    batch_number: str
    country_of_origin: str
    manufacturing_date: datetime
    expiry_date: datetime
    description: Optional[str] = None

class DrugResponse(DrugBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # For ORM models like SQLAlchemy


class NewDrugsListResponse(BaseModel):
    drugs: List[DrugResponse]
    total: int

    class Config:
        from_attributes = True


class DrugStatus(str, enum.Enum):
    active = "active"
    expired = "expired"

class ActiveDrugs(BaseModel):
    drug_name: str
    status: DrugStatus

class ExpiredDrugs(BaseModel):
    drug_name: str
    status: DrugStatus

class DrugDashboard(BaseModel):
    active: List[ActiveDrugs]
    expired: List[ExpiredDrugs]
    active_count: int
    expired_count: int
    total: int




