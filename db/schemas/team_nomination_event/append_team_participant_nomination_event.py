from pydantic import BaseModel, EmailStr

from db.schemas.nomination_event.nomination_event import NominationEventSchema
from db.schemas.nomination_event.nomination_event_type import NominationEventType


class AppendTeamParticipantNominationEventSchema(BaseModel):
    team_id: int
    participant_email: EmailStr
    nomination_name: str
    event_name: str
    nomination_event_type: NominationEventType
    software: str | None
    equipment: str | None

    def to_nomination_event_schema(self):
        return NominationEventSchema(
            event_name=self.event_name,
            nomination_name=self.nomination_name,
            type=self.nomination_event_type
        )
