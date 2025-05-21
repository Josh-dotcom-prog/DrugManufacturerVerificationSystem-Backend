from pydantic import BaseModel,constr, conint, EmailStr
import enum
from typing import Annotated


class UserRole(str, enum.Enum):
    admin = "admin"
    manufacturer = "manufacturer"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        raise ValueError(
            f"Invalid role: {value!r}. Allowed values: {[role.value for role in cls]}"
        )

# Regex explanation:
# - ^07\d{8}$ → local format, e.g., 0701234567
# - ^\+2567\d{8}$ → international format, e.g., +256701234567

UgandanPhoneNumber = Annotated[
    str,
    constr(pattern=r"^(07\d{8}|\+2567\d{8})$")
]

class UserBase(BaseModel):
    name: str
    license_number: str
    email: EmailStr
    phone_number: UgandanPhoneNumber
    street_address: str
    password: str
    certificate: str


class UserCreateSchema(UserBase):
    pass

class ActivateUserSchema(BaseModel):
    email: str
    token: str

class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserForgotPasswordSchema(BaseModel):
    email: str

class UserRestPasswordSchema(BaseModel):
    email: str
    token: str
    password: constr(min_length=8)

