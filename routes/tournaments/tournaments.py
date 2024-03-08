from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from sqlalchemy.sql.annotation import Annotated
from starlette.responses import Response

from db.schemas.nomination_event import NominationEventNameSchema
from dependencies import authorized_only, get_db
from routes.tournaments.tournaments_service import TournamentService

tournaments = APIRouter(prefix="/tournaments", tags=["tournaments"])


@tournaments.post("/start_group_tournament")
async def start_group_tournament(
        response: Response,
        nomination_event: NominationEventNameSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentService(db)
    return service.start_group_tournament(response, token, nomination_event)


@tournaments.post("/start_play_off_tournament")
async def start_play_off_tournament():
    pass
