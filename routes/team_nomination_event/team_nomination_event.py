from typing import Annotated

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from dependencies import authorized_only, get_db
from routes.team_nomination_event.team_nomination_event_service import TeamNominationEventService

team_nomination_event = APIRouter(
    prefix="/team_nomination_event",
    tags=["team_nomination_event"]
)


@team_nomination_event.get("/team_participant")
async def list_teams_nomination_event(
        response: Response,
        nomination_name: Annotated[str, Query()],
        event_name: Annotated[str, Query()],
        nomination_event_type: Annotated[str, Query()],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamNominationEventService(db)
    return service.list_teams_nomination_event(
        response,
        token,
        nomination_name,
        event_name,
        nomination_event_type
    )
