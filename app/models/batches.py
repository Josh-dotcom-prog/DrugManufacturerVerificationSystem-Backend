from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
import enum

class BatchStatus(enum.Enum):
    active = "active"
    recalled = "recalled"
    expired = "expired"

class Batch(Base):
    __tablename__ = 'batches'

    id = Column(Integer, primary_key=True)
    batch_number = Column(String, unique=True, nullable=False)
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'))
    manufacturing_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    status = Column(Enum(BatchStatus), default=BatchStatus.active)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    manufacturer = relationship('Manufacturer', back_populates='batches')
    drugs = relationship('Drug', back_populates='batch')
