from pydantic import BaseModel, Field


class NominationUpdateSchema(BaseModel):
    id: int
    new_name: str = Field(min_length=5)

    class Config:
        from_attributes = True
