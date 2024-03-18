import re
from enum import Enum
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, EmailStr, validator, Field


class UserRole(str, Enum):
    admin = "admin"
    judge = "judge"
    specialist = "specialist"


class UserSchema(BaseModel):
    email: EmailStr
    first_name: str
    second_name: str
    third_name: str
    phone: str
    role: UserRole
    educational_institution: str | None = None

    class Config:
        from_attributes = True

    @validator('phone')
    def validate_unique_phone_number(cls, value: str):
        pattern = re.compile(r'^\+\d{3}-\d{2}-\d{3}-\d{2}-\d{2}$')
        if pattern.match(value) is not None:
            return value
        raise ValueError(f"phone format is invalid, {value}")


class UserCreateSchema(UserSchema):
    password: str = Field(min_length=7)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserDatabaseSchema(UserSchema):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True


class EditUserSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(min_length=7, default=None)
    first_name: str | None = None
    second_name: str | None = None
    third_name: str | None = None
    phone: str | None = None
    educational_institution: str | None = None

    class Config:
        from_attributes = True

    @validator('phone')
    def validate_unique_phone_number(cls, value: str):
        if value is None:
            return value
        pattern = re.compile(r'^\+\d{3}-\d{2}-\d{3}-\d{2}-\d{2}$')
        if pattern.match(value) is not None:
            return value
        raise ValueError(f"phone format is invalid; valid example :: +375-22-222-22-22, {value}")
