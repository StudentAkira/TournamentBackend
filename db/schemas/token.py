from pydantic import BaseModel

from db.schemas.user import UserRole


class TokenDatabaseSchema(BaseModel):
    token: str
    owner_id: int


class TokenDecodedSchema(BaseModel):
    user_id: int
    exp: int
    role: UserRole
