from pydantic import BaseModel

from db.schemas.nomination_event.nomination_event_type import NominationEventType


class NominationEventParticipantCountSchema(BaseModel):
    nomination_name: str
    type: NominationEventType
    participant_count: int
