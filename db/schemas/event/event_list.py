from db.schemas.event.event import EventSchema
from db.schemas.nomination.nomination import NominationSchema


class EventListSchema(EventSchema):
    nominations: list[NominationSchema]

    class Config:
        from_attributes = True
