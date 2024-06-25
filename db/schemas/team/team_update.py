from pydantic import BaseModel, Field


class TeamUpdateSchema(BaseModel):
    id: int
    new_name: str = Field(min_length=3)

    class Config:
        from_attributes = True
