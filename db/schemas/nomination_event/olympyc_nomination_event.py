from pydantic import BaseModel


class OlympycNominationEventSchema(BaseModel):
    event_name: str
    nomination_name: str

