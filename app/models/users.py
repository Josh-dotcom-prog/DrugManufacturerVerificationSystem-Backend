from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, ForeignKey,LargeBinary ,Enum as SqlEnum
from app.database.database import Base
from sqlalchemy.orm import mapped_column, relationship
import enum


class UserRoleEnum(str, enum.Enum):
    admin = "admin"
    manufacturer = "manufacturer"

class ApprovalStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"




class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    license_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    street_address = Column(String, nullable=False)
    password = Column(String, nullable=False)  # Store hashed password!
    role = Column(SqlEnum(UserRoleEnum, name="user_role_enum"), nullable=False)
    certificate = Column(LargeBinary, nullable=False)  # Could be file path or Base64
    approval_status = Column(SqlEnum(ApprovalStatus, name="approval_status_enum"), nullable=False)

    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None, onupdate=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())

    tokens = relationship("UserToken", back_populates="user", cascade="all, delete")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete")
    drugs = relationship("Drug", back_populates="manufacturer", cascade="all, delete")

    def get_context_string(self, context: str):
        return f"{context}{self.password[-6:]}{self.updated_at.strftime('%m%d%Y%H%M%S')}".strip()



class UserToken(Base):
    __tablename__ = 'user_tokens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey('users.id'))
    access_key = Column(String(250), nullable=True, index=True, default=None)
    refresh_key = Column(String(250), nullable=True, index=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
    user = relationship("User", back_populates="tokens")


class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    token_hash = Column(String(255), nullable=False)  # Store the hashed token
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)  # Set expiration for token

    user = relationship("User", back_populates="password_reset_tokens")

    def __repr__(self):
        return f"<PasswordResetToken(user_id={self.user_id}, token_hash={self.token_hash})>"
