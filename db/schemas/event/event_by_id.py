from pydantic import BaseModel

from db.schemas.event.event_list import EventListSchema


class EventByIdSchema(BaseModel):
    edit_access: bool
    event_data: EventListSchema
