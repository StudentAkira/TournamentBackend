from db.schemas.event.event import EventSchema
from db.schemas.nomination.nomination_get import NominationGetSchema


class EventListSchema(EventSchema):
    nominations: list[NominationGetSchema]

    class Config:
        from_attributes = True
