from pydantic import BaseModel


class ListTeamsOfNominationEventSchema(BaseModel):
    nomination_name: str
    event_name: str
