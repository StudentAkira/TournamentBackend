from pydantic import BaseModel, Field, EmailStr

from db.schemas.participant import ParticipantSchema


class TeamSchema(BaseModel):
    name: str = Field(min_length=3)

    class Config:
        from_attributes = True


class TeamUpdateSchema(BaseModel):
    old_name: str = Field(min_length=3)

    new_name: str = Field(min_length=3)

    class Config:
        from_attributes = True

