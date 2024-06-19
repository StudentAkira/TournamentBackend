from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema
from db.schemas.team.team import TeamSchema
from dependencies.dependencies import authorized_only, get_db
from routes.tournaments.tournaments_service import TournamentService
from urls import URLs

tournaments = APIRouter(prefix=URLs.tournaments_prefix.value, tags=URLs.tournaments_tags.value)


@tournaments.get(URLs.get_groups_of_tournament.value)
async def get_groups_of_tournament(
        response: Response,
        nomination_event: OlympycNominationEventSchema = Depends(),
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentService(db)
    return service.get_groups_of_tournament(response, token, nomination_event)


@tournaments.post(URLs.start_group_stage.value)
async def start_group_stage(
        response: Response,
        nomination_event: OlympycNominationEventSchema,
        group_count: int = Body(gt=0),
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentService(db)
    return service.start_group_stage(response, token, nomination_event, group_count)


@tournaments.post(URLs.finish_group_stage.value)
async def finish_group_stage(
    response: Response,
    nomination_event: OlympycNominationEventSchema,
    token: str = Depends(authorized_only),
    db: Session = Depends(get_db)
):
    service = TournamentService(db)
    return service.finish_group_stage(response, token, nomination_event)


@tournaments.post(URLs.start_play_off_stage.value)
async def start_play_off_stage(
        response: Response,
        nomination_event: OlympycNominationEventSchema,
        teams: list[TeamSchema],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentService(db)
    return service.start_play_off_tournament(response, token, nomination_event, teams)


@tournaments.post(URLs.finish_play_off_stage.value)
async def finish_play_off_stage(
        response: Response,
        nomination_event: OlympycNominationEventSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentService(db)
    return service.finish_play_off_stage(response, token, nomination_event)
