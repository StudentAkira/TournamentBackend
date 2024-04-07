import datetime

from pydantic import BaseModel


class EventUpdateSchema(BaseModel):
    old_name: str

    new_name: str
    new_date: datetime.date
