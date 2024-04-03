from typing import Annotated
from fastapi import APIRouter, Query, Depends
from starlette.responses import Response
from sqlalchemy.orm import Session

from db.schemas.match import SetMatchResultSchema
from db.schemas.nomination_event import NominationEventSchema
from dependencies import authorized_only, get_db
from routes.match.match_service import MatchService

match = APIRouter(prefix="/api/match", tags=["match"])


@match.get("/get_matches_of_tournament")
async def get_group_matches_of_tournament(
        response: Response,
        nomination_event: NominationEventSchema = Depends(),
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = MatchService(db)
    return service.get_group_matches_of_tournament(response, token, nomination_event)


@match.post("/set_match_result")
async def set_match_result(
        response: Response,
        data: SetMatchResultSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = MatchService(db)
    return service.set_match_result(response, token, data)
