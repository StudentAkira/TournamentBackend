from pydantic import BaseModel

from db.schemas.nomination_event.nomination_event_type import NominationEventType
from db.schemas.team_participant.team_participant import TeamParticipantsSchema


class NominationEventFullInfoSchema(BaseModel):
    event_name: str
    nomination_name: str
    type: NominationEventType

    teams: list[TeamParticipantsSchema]

    class Config:
        from_attributes = True
