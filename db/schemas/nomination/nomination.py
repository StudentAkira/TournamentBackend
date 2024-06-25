from pydantic import BaseModel, Field


class NominationSchema(BaseModel):
    id: int
    name: str = Field(min_length=5)

    class Config:
        from_attributes = True
