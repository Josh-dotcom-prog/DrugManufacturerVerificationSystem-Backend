from app.database.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum, ForeignKey, func
from sqlalchemy.orm import relationship
import enum

class CategoryEnum(str, enum.Enum):
    antibiotic = "antibiotic"
    analgesic = "analgesic"
    antiviral = "antiviral"
    antidiabetic = "antidiabetic"
    antihistamine = "antihistamine"
    antihypertensive = "antihypertensive"


class DosageFormEnum(str, enum.Enum):
    tablet = "tablet"
    capsule = "capsule"
    syrup = "syrup"
    injection = "injection"
    cream = "cream"
    ointment = "ointment"


class Drug(Base):
    __tablename__ = "drugs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(SqlEnum(CategoryEnum, name="category_enum", create_constraint=True), nullable=False)
    dosage_form = Column(SqlEnum(DosageFormEnum, name="dosage_form_enum", create_constraint=True), nullable=False)

    manufacturer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    manufacturer = relationship("User", back_populates="drugs")

    batch_number = Column(String, unique=True, nullable=False)
    country_of_origin = Column(String, nullable=False)
    manufacturing_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    description = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
