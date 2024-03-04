from pydantic import BaseModel, Field

from db.schemas.participant import ParticipantSchema


class TeamSchema(BaseModel):
    name: str = Field(min_length=3)

    class Config:
        from_attributes = True


class TeamParticipantsSchema(BaseModel):
    name: str
    participants: list[ParticipantSchema]

    class Config:
        from_attributes = True
