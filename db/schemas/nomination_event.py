from enum import Enum

from pydantic import BaseModel

from db.schemas.team import TeamParticipantsSchema


class NominationEventType(str, Enum):
    olympyc = "olympyc"
    time = "time"
    criteria = "criteria"


class NominationEventNameSchema(BaseModel):
    event_name: str
    nomination_name: str


class NominationEventSchema(NominationEventNameSchema):

    teams: list[TeamParticipantsSchema]

    class Config:
        from_attributes = True


