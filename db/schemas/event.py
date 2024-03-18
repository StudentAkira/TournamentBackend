import datetime

from pydantic import BaseModel, Field
from db.schemas.nomination import NominationSchema
from db.schemas.nomination_event import NominationEventType


class EventSchema(BaseModel):
    name: str = Field(min_length=5)
    date: datetime.date

    class Config:
        from_attributes = True


class EventGetNameSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class EventDeleteSchema(BaseModel):
    name: str


class EventCreateSchema(BaseModel):
    name: str = Field(min_length=5)
    date: datetime.date

    class Config:
        from_attributes = True


class EventUpdateSchema(BaseModel):
    old_name: str

    new_name: str
    new_date: datetime.date


class EventListSchema(EventSchema):
    nominations: list[NominationSchema]
