from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.team import TeamSchema
from dependencies import get_db, authorized_only
from routes.teams.teams_service import TeamsService

teams = APIRouter(prefix="/teams", tags=["teams"])


@teams.post("/teams")
async def create_team(
        response: Response,
        team: TeamSchema,
        participants_emails: list[EmailStr],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamsService(db)
    return service.create_team(response, token, team, participants_emails)


@teams.get("/teams")
async def get_teams(
        response: Response,
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamsService(db)
    return service.get_teams_by_owner(response, token, offset, limit)
