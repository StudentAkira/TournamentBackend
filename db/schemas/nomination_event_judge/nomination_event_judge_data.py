from pydantic import BaseModel, EmailStr

from db.schemas.nomination_event.nomination_event_type import NominationEventType


class NominationEventJudgeDataSchema(BaseModel):
    nomination_id: int
    event_id: int
    nomination_event_type: NominationEventType | None = NominationEventType.olympyc

    judge_id: int
