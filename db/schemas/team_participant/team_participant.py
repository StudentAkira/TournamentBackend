from pydantic import BaseModel

from db.schemas.participant.participant_get import ParticipantGetSchema


class TeamParticipantsSchema(BaseModel):
    name: str
    participants: list[ParticipantGetSchema]

    class Config:
        from_attributes = True
