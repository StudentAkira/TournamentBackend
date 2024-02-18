from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str


class UserGet(BaseUser):
    first_name: str
    second_name: str
    third_name: str

    region: str


class UserCreate(BaseUser):
    password: str


class UserLogin(BaseUser):
    password: str

