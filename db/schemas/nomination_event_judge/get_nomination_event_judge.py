from typing import Annotated

from fastapi import Query
from pydantic import BaseModel

from db.schemas.nomination_event.nomination_event_type import NominationEventType


class GetNominationEventJudgeSchema(BaseModel):
    nomination_id: Annotated[int, Query()]
    event_id: Annotated[int, Query()]
    nomination_event_type: Annotated[NominationEventType | None, Query(default=NominationEventType.olympyc)]
