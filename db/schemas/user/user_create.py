from pydantic import Field

from db.schemas.user.user import UserSchema


class UserCreateSchema(UserSchema):
    password: str = Field(min_length=7)

