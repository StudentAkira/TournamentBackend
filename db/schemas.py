from pydantic import BaseModel, Field
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    judge = "judge"


class BaseUser(BaseModel):
    username: str = Field(min_length=5)


class UserGet(BaseUser):
    first_name: str = Field(min_length=1)
    second_name: str = Field(min_length=1)
    third_name: str = Field(min_length=1)

    region: str = Field(min_length=1)
    role: UserRole


class UserCreate(UserGet):
    password: str


class UserLogin(BaseUser):
    password: str


class UserDB(UserGet):
    id: int
    hashed_password: str
