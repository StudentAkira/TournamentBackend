from pydantic import BaseModel, Field


class TeamSchema(BaseModel):
    id: int

    class Config:
        from_attributes = True
