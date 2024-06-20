import datetime

from pydantic import BaseModel


class EventUpdateSchema(BaseModel):
    id: int

    new_name: str
    new_date: datetime.date
