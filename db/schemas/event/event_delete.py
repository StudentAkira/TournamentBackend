from pydantic import BaseModel


class EventDeleteSchema(BaseModel):
    name: str
