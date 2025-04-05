from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base  # assuming you have a Base from your SQLAlchemy setup

class Manufacturer(Base):
    __tablename__ = 'manufacturers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    license_number = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    contact_email = Column(String, nullable=False)
    contact_phone = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    license_file = Column(String, nullable=True)
    certificate_file = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # batches = relationship('Batch', back_populates='manufacturer')
