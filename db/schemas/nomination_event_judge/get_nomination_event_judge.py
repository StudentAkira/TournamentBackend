from typing import Annotated

from fastapi import Query
from pydantic import BaseModel

from db.schemas.nomination_event.nomination_event_type import NominationEventType


class GetNominationEventJudgeSchema(BaseModel):
    nomination_name: Annotated[str, Query()]
    event_name: Annotated[str, Query()]
    nomination_event_type: Annotated[NominationEventType, Query()]
