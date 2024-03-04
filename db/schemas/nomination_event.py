from pydantic import BaseModel


class NominationEventSchema(BaseModel):
    event_name: str
    nomination_name: str

    class Config:
        from_attributes = True
