from pydantic import BaseModel
from db.schemas.nomination_event.nomination_event_type import NominationEventType


class NominationEventAppendSchema(BaseModel):
    event_id: int
    nomination_name: str
    type: NominationEventType | None = NominationEventType.olympyc
