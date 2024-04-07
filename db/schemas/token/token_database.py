from pydantic import BaseModel


class TokenDatabaseSchema(BaseModel):
    token: str
    owner_id: int
