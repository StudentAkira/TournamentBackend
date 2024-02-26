from enum import Enum
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    admin = "admin"
    judge = "judge"
    specialist = "specialist"


class UserSchema(BaseModel):
    email: EmailStr
    first_name: str
    second_name: str
    third_name: str
    phone: PhoneNumber
    role: UserRole
    educational_institution: str | None = None

    class Config:
        from_attributes = True


class UserCreateSchema(UserSchema):
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserDatabaseSchema(UserSchema):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True
