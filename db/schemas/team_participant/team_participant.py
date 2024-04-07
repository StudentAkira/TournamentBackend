from pydantic import BaseModel

from db.schemas.participant.participant import ParticipantSchema


class TeamParticipantsSchema(BaseModel):
    name: str
    participants: list[ParticipantSchema]

    class Config:
        from_attributes = True
