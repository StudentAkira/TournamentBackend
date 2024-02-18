from pydantic import BaseModel, Field
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    judge = "judge"


class BaseUser(BaseModel):
    username: str


class UserGet(BaseUser):
    first_name: str
    second_name: str
    third_name: str

    region: str
    role: UserRole


class UserCreate(UserGet):
    password: str


class UserLogin(BaseUser):
    password: str


class UserDB(UserGet):
    id: int
    hashed_password: str
