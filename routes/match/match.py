from fastapi import APIRouter, Depends
from starlette.responses import Response
from sqlalchemy.orm import Session

from db.schemas.match.set_match_result_schema import SetMatchResultSchema
from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema
from dependencies.dependencies import authorized_only, get_db
from routes.match.match_service import MatchService
from urls import URLs

match = APIRouter(prefix=URLs.match_prefix.value, tags=URLs.match_tags.value)


@match.get(URLs.get_group_matches.value)
async def get_group_matches_of_tournament(
        response: Response,
        nomination_event: OlympycNominationEventSchema = Depends(),
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = MatchService(db)
    return service.get_group_matches(response, token, nomination_event)


@match.get(URLs.get_bracket_matches.value)
async def get_bracket_matches_of_tournament(
        response: Response,
        nomination_event: OlympycNominationEventSchema = Depends(),
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = MatchService(db)
    return service.get_bracket_matches(response, token, nomination_event)


@match.post(URLs.set_group_match_result.value)
async def set_group_match_result(
        response: Response,
        data: SetMatchResultSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = MatchService(db)
    return service.set_group_match_result(response, token, data)


@match.post(URLs.set_bracket_match_result.value)
async def set_bracket_match_result(
        response: Response,
        data: SetMatchResultSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = MatchService(db)
    return service.set_bracket_match_result(response, token, data)
