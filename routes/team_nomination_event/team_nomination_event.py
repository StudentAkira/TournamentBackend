from typing import Annotated
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event.nomination_event import NominationEventSchema
from dependencies import authorized_only, get_db
from routes.team_nomination_event.team_nomination_event_service import TeamNominationEventService

team_nomination_event = APIRouter(
    prefix="/api/team_nomination_event",
    tags=["team_nomination_event"]
)


@team_nomination_event.get("/team_participant")
async def list_teams_nomination_event(
        response: Response,
        nomination_event: NominationEventSchema = Depends(),
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamNominationEventService(db)
    return service.list_teams_nomination_event(
        response,
        token,
        nomination_event
    )
