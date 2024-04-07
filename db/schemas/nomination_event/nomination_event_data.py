import datetime

from pydantic import BaseModel

from db.schemas.nomination_event.nomination_event_participant_count import NominationEventParticipantCountSchema


class NominationEventDataSchema(BaseModel):
    name: str
    date: datetime.date

    nominations: list[NominationEventParticipantCountSchema]
