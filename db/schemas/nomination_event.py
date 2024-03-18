import datetime
from enum import Enum
from pydantic import BaseModel

from db.schemas.team_participant import TeamParticipantsSchema


class NominationEventType(str, Enum):
    olympyc = "olympyc"
    time = "time"
    criteria = "criteria"


class NominationEventParticipantCountSchema(BaseModel):
    name: str
    participant_count: int

    type: NominationEventType


class NominationEventSchema(BaseModel):
    event_name: str
    nomination_name: str


class NominationEventDataSchema(BaseModel):
    name: str
    date: datetime.date

    nominations: list[NominationEventParticipantCountSchema]


class NominationEventFullInfoSchema(BaseModel):
    event_name: str
    nomination_name: str
    type: NominationEventType

    teams: list[TeamParticipantsSchema]

    class Config:
        from_attributes = True


class NominationEventDeleteSchema(BaseModel):
    event_name: str
    nomination_name: str


