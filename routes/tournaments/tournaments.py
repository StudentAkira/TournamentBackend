from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.group_tournament import StartGroupTournamentSchema
from db.schemas.nomination_event import NominationEventSchema
from dependencies import authorized_only, get_db
from routes.tournaments.tournaments_service import TournamentService

tournaments = APIRouter(prefix="/tournaments", tags=["tournaments"])


@tournaments.post("/start_group_tournament")
async def start_group_tournament(
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
        nomination_event: NominationEventSchema = Depends(),
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentService(db)
    return service.get_groups_of_tournament(response, token, nomination_event)


@tournaments.post("/start_play_off_tournament")
async def start_play_off_tournament():
    pass
