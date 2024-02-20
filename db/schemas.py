from pydantic import BaseModel, Field, EmailStr
from enum import Enum

from pydantic_extra_types.phone_numbers import PhoneNumber


class UserRole(str, Enum):
    admin = "admin"
    judge = "judge"
    specialist = "specialist"


email: EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    first_name: str
    second_name: str
    third_name: str
    phone: PhoneNumber
    role: UserRole
    region: str
    educational_institution: str | None = None


class CreateUser(BaseUser):
    password: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class DatabaseUser(BaseUser):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True


class TokenDB(BaseModel):
    token: str
    owner_id: int


class DecodedToken(BaseUser):
    user_id: int
    exp: int
