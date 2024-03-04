from pydantic import BaseModel


class NominationEvent(BaseModel):
    event_name: str
