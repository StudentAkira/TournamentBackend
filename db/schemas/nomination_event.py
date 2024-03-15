import datetime
from enum import Enum
from pydantic import BaseModel

from db.schemas.nomination import NominationSchema, NominationParticipantCountSchema
from db.schemas.team_participant import TeamParticipantsSchema


class NominationEventType(str, Enum):
    olympyc = "olympyc"
    time = "time"
    criteria = "criteria"


class NominationEventSchema(BaseModel):
    event_name: str
    nomination_name: str


class NominationEventDataSchema(BaseModel):
    name: str
    date: datetime.date

    nominations: list[NominationParticipantCountSchema]


class NominationEventFullInfoSchema(BaseModel):
    event_name: str
    nomination_name: str

    teams: list[TeamParticipantsSchema]

    class Config:
        from_attributes = True


class NominationEventDeleteSchema(BaseModel):
    event_name: str
    nomination_name: str
