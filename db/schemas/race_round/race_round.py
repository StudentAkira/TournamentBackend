from pydantic import BaseModel

from db.schemas.nomination_event.time_nomination_event import TimeNominationEventSchema


class RaceRoundSchema(BaseModel):
    nomination_event: TimeNominationEventSchema
