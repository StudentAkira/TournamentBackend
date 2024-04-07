from pydantic import BaseModel

from db.schemas.user.user_role import UserRole


class TokenDecodedSchema(BaseModel):
    user_id: int
    exp: int
    role: UserRole
