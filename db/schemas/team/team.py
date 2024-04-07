from pydantic import BaseModel, Field


class TeamSchema(BaseModel):
    name: str = Field(min_length=3)

    class Config:
        from_attributes = True
