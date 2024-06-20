from pydantic import BaseModel, Field


class TeamCreateSchema(BaseModel):
    name: str = Field(min_length=3)
    participants_ids: list[int]

    class Config:
        from_attributes = True
