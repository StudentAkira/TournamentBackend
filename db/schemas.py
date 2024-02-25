import datetime

from pydantic import BaseModel, EmailStr, Field
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
        from_attributes = True


class TokenDB(BaseModel):
    token: str
    owner_id: int


class DecodedToken(BaseUser):
    user_id: int
    exp: int


class Event(BaseModel):
    name: str = Field(min_length=5)

    class Config:
        from_attributes=True


class BaseNomination(BaseModel):
    name: str = Field(min_length=5)

    class Config:
        from_attributes = True


class EventCreate(Event):
    nominations: list[BaseNomination] | None


class Software(BaseModel):
    name: str = Field(min_length=3)


class Equipment(BaseModel):
    name: str = Field(min_length=3)


class Participant(BaseModel):
    participant_email: EmailStr
    first_name: str
    second_name: str
    third_name: str
    region: str
    birth_date: datetime.date
    software: list[Software] | None
    equipment: list[Equipment] | None
    educational_institution: str
    additional_educational_institution: str
    supervisor_first_name: str
    supervisor_second_name: str
    supervisor_third_name: str

class Team(BaseModel):
    name: str = Field(min_length=3)

    class Config:
        from_attributes = True


