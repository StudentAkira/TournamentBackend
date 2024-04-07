import re

from pydantic import BaseModel, EmailStr, validator

from db.schemas.user.user_role import UserRole


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
