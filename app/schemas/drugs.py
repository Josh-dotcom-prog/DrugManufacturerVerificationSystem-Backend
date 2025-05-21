from pydantic import BaseModel, model_validator, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum



class Category(str, Enum):
    antibiotic = "antibiotic"
    analgesic = "analgesic"
    antiviral = "antiviral"
    antidiabetic = "antidiabetic"
    antihistamine = "antihistamine"
    antihypertensive = "antihypertensive"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return super()._missing_(value)


class DosageForm(str, Enum):
    tablet = "tablet"
    capsule = "capsule"
    syrup = "syrup"
    injection = "injection"
    cream = "cream"
    ointment = "ointment"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return super()._missing_(value)


class DrugCreate(BaseModel):
    name: str
    category: Category
    dosage_form: DosageForm
    manufacturer: str
    batch_number: str
    country_of_origin: str
    manufacturing_date: datetime
    expiry_date: datetime
    description: str

    @model_validator(mode='after')
    def validate_dates(self) -> 'DrugCreate':
        if self.manufacturing_date >= self.expiry_date:
            raise ValueError('Manufacturing date must be before expiry date')
        return self


class DrugUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    category: Optional[Category] = None
    dosage_form: Optional[DosageForm] = None
    batch_number: Optional[str] = None
    country_of_origin: Optional[str] = None
    manufacturing_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    description: Optional[str] = None

    @model_validator(mode='after')
    def validate_dates(self) -> 'DrugUpdate':
        if self.manufacturing_date and self.expiry_date:
            if self.manufacturing_date >= self.expiry_date:
                raise ValueError("Manufacturing date must be before expiry date")
        return self