from typing import Annotated

from fastapi import APIRouter, Depends, Body
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.team import TeamToEventNominationSchema
from dependencies import get_db, authorized_only
from routes.tournament_registration.tournament_registration_service import TournamentRegistrationService

tournament_registration = APIRouter(prefix="/tournament_registration", tags=["tournament_registration"])


@tournament_registration.post("/nomination_event_team")
async def append_team_to_nomination_event(
        response: Response,
        team_nomination_event_data: TeamToEventNominationSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentRegistrationService(db)
    return service.append_team_to_event_nomination(
        response,
        token,
        team_nomination_event_data
    )


