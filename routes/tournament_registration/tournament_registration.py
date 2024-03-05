from typing import Annotated

from fastapi import APIRouter, Depends, Body, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import Response

from dependencies import get_db, authorized_only
from routes.tournament_registration.tournament_registration_service import TournamentRegistrationService

tournament_registration = APIRouter(prefix="/tournament_registration", tags=["tournament_registration"])


@tournament_registration.post("/nomination_event_team")
async def append_team_to_nomination_event(
        response: Response,
        team_name_or_participant_email: Annotated[str | EmailStr, Body()],
        event_name: Annotated[str, Body()],
        nomination_name: Annotated[str, Body()],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentRegistrationService(db)
    return service.append_team_to_event_nomination(response, token, team_name_or_participant_email, nomination_name, event_name)


@tournament_registration.get('/teams_of_nomination_event')
async def get_teams_of_nomination_event(
        response: Response,
        nomination_name: Annotated[str, Query()],
        event_name: Annotated[str, Query()],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentRegistrationService(db)
    return service.get_teams_of_nomination_event(response, token, nomination_name, event_name)


@tournament_registration.get("/nomination_event_full_info")
async def get_nominations_events_full_info(
        response: Response,
        offset: Annotated[int, Query()],
        limit: Annotated[int, Query()],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentRegistrationService(db)
    return service.get_nomination_events_full_info(response, token, offset, limit)


@tournament_registration.get("/nomination_event_names")
async def get_nominations_events_names(
        response: Response,
        offset: Annotated[int, Query()],
        limit: Annotated[int, Query()],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentRegistrationService(db)
    return service.get_nomination_events_names(response, token, offset, limit)
