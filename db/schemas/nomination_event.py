import datetime
from enum import Enum
from pydantic import BaseModel

from db.schemas.participant import ParticipantPDFSchema
from db.schemas.team_participant import TeamParticipantsSchema


class NominationEventType(str, Enum):
    olympyc = "olympyc"
    time = "time"
    criteria = "criteria"


class NominationEventParticipantCountSchema(BaseModel):
    nomination_name: str
    type: NominationEventType
    participant_count: int


class NominationEventSchema(BaseModel):
    event_name: str
    nomination_name: str
    type: NominationEventType


class OlympycNominationEventSchema(BaseModel):
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
    type: NominationEventType


class NominationEventPDFSchema(BaseModel):
    nomination_name: str
    event_name: str
    type: str
    participants: list[ParticipantPDFSchema]

    first_name: str
    second_name: str
    third_name: str
    region: str
