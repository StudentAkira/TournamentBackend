from pydantic import BaseModel

from db.schemas.nomination_event.nomination_event_type import NominationEventType


class NominationEventDeleteSchema(BaseModel):
    event_name: str
    nomination_name: str
    type: NominationEventType
