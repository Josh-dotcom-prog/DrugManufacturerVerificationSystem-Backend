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


######################################################################################################

# THIS WAS A QUICK FIX, IT'S UGLY BUT BARE WITH IT. I CAN SEE YOU SCREAMING DRY!!!!!


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

class DrugResponseWithStatus(BaseModel):
    id: int
    name: str
    category: Category
    dosage_form: DosageForm
    manufacturer: str
    batch_number: str
    country_of_origin: str
    description: Optional[str] = None
    status: DrugStatus
    manufacturing_date: datetime
    expiry_date: datetime
    created_at: datetime
    updated_at: datetime





