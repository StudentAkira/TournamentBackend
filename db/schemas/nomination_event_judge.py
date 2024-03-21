from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, EmailStr

from db.schemas.nomination_event import NominationEventType
from db.schemas.user import UserSchema


class NominationEventJudgeDataSchema(BaseModel):
    nomination_name: str
    event_name: str
    nomination_event_type: NominationEventType

    email: EmailStr


class GenNominationEventJudgeSchema(BaseModel):
    nomination_name: Annotated[str, Query()]
    event_name: Annotated[str, Query()]
    nomination_event_type: Annotated[NominationEventType, Query()]


class NominationEventJudgesSchema(BaseModel):
    judges: list[UserSchema]
