from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base


class Drug(Base):
    __tablename__ = 'drugs'

    id = Column(Integer, primary_key=True)
    serial_number = Column(String, unique=True, nullable=False)
    batch_id = Column(Integer, ForeignKey('batches.id'))
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    qr_code = Column(String, unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    batch = relationship('Batch', back_populates='drugs')
    verifications = relationship('Verification', back_populates='drug')
