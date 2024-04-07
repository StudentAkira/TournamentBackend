from pydantic import BaseModel, EmailStr

from db.schemas.nomination_event.nomination_event_type import NominationEventType


class AppendTeamParticipantNominationEventSchema(BaseModel):
    team_name: str | EmailStr
    participant_email: EmailStr
    nomination_name: str
    event_name: str
    nomination_event_type: NominationEventType
    software: str | None
    equipment: str | None
