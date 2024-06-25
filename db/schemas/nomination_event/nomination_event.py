from pydantic import BaseModel
from db.schemas.nomination_event.nomination_event_type import NominationEventType


class NominationEventSchema(BaseModel):
    event_id: int
    nomination_id: int
    type: NominationEventType | None = NominationEventType.olympyc
