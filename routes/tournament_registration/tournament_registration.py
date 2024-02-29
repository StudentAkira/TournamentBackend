from typing import Annotated

from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from dependencies import get_db, authorized_only
from routes.tournament_registration.tournament_registration_service import TournamentRegistrationService

tournament_registration = APIRouter(prefix="/tournament_registration", tags=["tournament_registration"])


@tournament_registration.post("/nomination_event")
async def append_team_to_nomination_event(
        response: Response,
        team_name: Annotated[str, Body()],
        event_name: Annotated[str, Body()],
        nomination_name: Annotated[str, Body()],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentRegistrationService(db)
    return service.append_team_to_event_nomination(response, token, team_name, nomination_name, event_name)


@tournament_registration.get('/nomination_event_teams')
async def get_nomination_event_teams(
        response: Response,
        nomination_name: Annotated[str, Query()],
        event_name: Annotated[str, Query()],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentRegistrationService(db)
    return service.get_teams_of_event_nomination(response, token, nomination_name, event_name)
