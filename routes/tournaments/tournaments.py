from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.group_tournament import StartGroupTournamentSchema
from db.schemas.nomination_event import OlympycNominationEventSchema
from db.schemas.team import TeamSchema
from dependencies import authorized_only, get_db
from routes.tournaments.tournaments_service import TournamentService

tournaments = APIRouter(prefix="/api/tournaments", tags=["tournaments"])


@tournaments.post("/start_group_stage")
async def start_group_stage(
        response: Response,
        nomination_event: StartGroupTournamentSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentService(db)
    return service.create_group_tournament(response, token, nomination_event)


@tournaments.get("/get_groups_of_tournament")
async def get_groups_of_tournament(
        response: Response,
        nomination_event: OlympycNominationEventSchema = Depends(),
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentService(db)
    return service.get_groups_of_tournament(response, token, nomination_event)


@tournaments.post("/finish_group_stage")
async def finish_group_stage(
    response: Response,
    nomination_event: OlympycNominationEventSchema,
    token: str = Depends(authorized_only),
    db: Session = Depends(get_db)
):
    service = TournamentService(db)
    return service.finish_group_stage(response, token, nomination_event)


@tournaments.post("/start_play_off_stage")
async def start_play_off_stage(
        response: Response,
        nomination_event: OlympycNominationEventSchema,
        teams: list[TeamSchema],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentService(db)
    return service.start_play_off_tournament(response, token, nomination_event, teams)


@tournaments.post("/finish_play_off_stage")
async def start_play_off_stage(
        response: Response,
        nomination_event: OlympycNominationEventSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentService(db)
    return service.finish_play_off_stage(response, token, nomination_event)
