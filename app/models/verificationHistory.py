from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base


class Verification(Base):
    __tablename__ = 'verifications'

    id = Column(Integer, primary_key=True)
    drug_id = Column(Integer, ForeignKey('drugs.id'))
    location = Column(String, nullable=False)
    device_info = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    is_authentic = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # drug = relationship('Drug', back_populates='verifications')
