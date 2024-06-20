from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event.nomination_event_type import NominationEventType
from db.schemas.nomination_event_judge.get_nomination_event_judge import GetNominationEventJudgeSchema
from db.schemas.nomination_event_judge.nomination_event_judge_data import NominationEventJudgeDataSchema
from dependencies.dependencies import authorized_only, get_db
from routes.nomination_event_judge.nomination_event_judge_service import NominationEventJudgeService
from urls import URLs

nomination_event_judge = APIRouter(prefix=URLs.nomination_evnet_judge.value, tags=URLs.nomination_event_judge_tags.value)


@nomination_event_judge.post(URLs.nomination_event_judge.value)
async def crete_nomination_event_judge(
        response: Response,
        data: NominationEventJudgeDataSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventJudgeService(db)
    return service.append_judge_to_nomination_event(response, token, data)


@nomination_event_judge.get(URLs.nomination_event_judge.value)
async def get_nomination_event_judges(
        response: Response,
        data: GetNominationEventJudgeSchema = Depends(),
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventJudgeService(db)
    return service.get_nomination_event_judges(response, token, data)


@nomination_event_judge.delete(URLs.nomination_event_judge.value)
async def delete_nomination_event_judge(
        response: Response,
        data: NominationEventJudgeDataSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventJudgeService(db)
    return service.delete_judge_from_nomination_event(response, token, data)
