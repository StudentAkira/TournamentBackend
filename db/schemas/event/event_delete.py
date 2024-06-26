from pydantic import BaseModel


class EventDeleteSchema(BaseModel):
    id: int
