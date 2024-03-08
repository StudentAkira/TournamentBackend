import datetime

from pydantic import BaseModel, Field
from db.schemas.nomination import NominationSchema
from db.schemas.nomination_event import NominationEventType


class EventSchema(BaseModel):
    name: str = Field(min_length=5)
    date: datetime.date

    class Config:
        from_attributes = True


class EventCreateSchema(EventSchema):
    nominations: list[tuple[NominationSchema, NominationEventType]] | None


class EventListSchema(EventSchema):
    nominations: list[NominationSchema]
