from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.team_nomination_event import AppendTeamToEventNominationSchema, ListTeamsOfNominationEventSchema, \
    UpdateTeamOfNominationEventSchema, DeleteTeamFromNominationEvent
from dependencies import get_db, authorized_only
from routes.tournament_registration.tournament_registration_service import TournamentRegistrationService

tournament_registration = APIRouter(prefix="/tournament_registration", tags=["tournament_registration"])


@tournament_registration.post("/nomination_event_team")
async def append_team_to_nomination_event(
        response: Response,
        team_nomination_event_data: AppendTeamToEventNominationSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentRegistrationService(db)
    return service.append_team_to_event_nomination(
        response,
        token,
        team_nomination_event_data
    )


@tournament_registration.get("/nomination_event_team")
async def list_teams_of_nomination_event(
        response: Response,
        nomination_name: Annotated[str, Query()],
        event_name: Annotated[str, Query()],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentRegistrationService(db)
    return service.list_teams_of_nomination_event(response, token, nomination_name, event_name)


@tournament_registration.put("/nomination_event_team")
async def update_team_of_nomination_event(
        response: Response,
        team_nomination_event_data: UpdateTeamOfNominationEventSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentRegistrationService(db)
    return service.update_team_of_nomination_event(response, token, team_nomination_event_data)


@tournament_registration.delete("/nomination_event_team")
async def delete_team_from_nomination_event(
        response: Response,
        team_nomination_event_data: DeleteTeamFromNominationEvent,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TournamentRegistrationService(db)
    return service.delete_team_to_event_nomination(
        response,
        token,
        team_nomination_event_data
    )
