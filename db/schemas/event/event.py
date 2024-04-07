import datetime

from pydantic import BaseModel, Field


class EventSchema(BaseModel):
    name: str = Field(min_length=5)
    date: datetime.date

    class Config:
        from_attributes = True
