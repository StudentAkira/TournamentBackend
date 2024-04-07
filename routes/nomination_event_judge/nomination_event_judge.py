from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event.nomination_event_type import NominationEventType
from db.schemas.nomination_event_judge.get_nomination_event_judge import GenNominationEventJudgeSchema
from db.schemas.nomination_event_judge.nomination_event_judge_data import NominationEventJudgeDataSchema
from dependencies import authorized_only, get_db
from routes.nomination_event_judge.nomination_event_judge_service import NominationEventJudgeService

nomination_event_judge = APIRouter(prefix="/api/nomination_event_judge", tags=["nomination_event_judge"])


@nomination_event_judge.post("/nomination_event_judge")
async def crete_nomination_event_judge(
        response: Response,
        data: NominationEventJudgeDataSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventJudgeService(db)
    return service.append_judge_to_nomination_event(response, token, data)


@nomination_event_judge.get("/nomination_event_judge")
async def get_nomination_event_judges(
        response: Response,
        nomination_name: Annotated[str, Query()],
        event_name: Annotated[str, Query()],
        nomination_event_type: Annotated[NominationEventType, Query()],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    data = GenNominationEventJudgeSchema(
        nomination_name=nomination_name,
        event_name=event_name,
        nomination_event_type=nomination_event_type
    )
    service = NominationEventJudgeService(db)
    return service.get_nomination_event_judges(
        response,
        token,
        data
    )


@nomination_event_judge.delete("/nomination_event_judge")
async def delete_nomination_event_judge(
        response: Response,
        data: NominationEventJudgeDataSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventJudgeService(db)
    return service.delete_judge_from_nomination_event(response, token, data)
