from pydantic import BaseModel

from db.schemas.nomination_event.nomination_event import NominationEventSchema
from db.schemas.nomination_event.nomination_event_type import NominationEventType


class TimeNominationEventSchema(BaseModel):
    event_name: str
    nomination_name: str

    def to_nomination_event_schema(self):
        return NominationEventSchema(
            **self.model_dump(),
            type=NominationEventType.time
        )
