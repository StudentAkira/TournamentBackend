from pydantic import BaseModel, Field


class NominationSchema(BaseModel):
    name: str = Field(min_length=5)

    class Config:
        from_attributes = True
