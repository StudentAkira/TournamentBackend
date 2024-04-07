from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.team.team import TeamSchema
from db.schemas.team.team_update import TeamUpdateSchema
from dependencies import get_db, authorized_only
from routes.team.teams_service import TeamsService

teams = APIRouter(prefix="/api/team", tags=["team"])


@teams.post("/teams")
async def create_team(
        response: Response,
        team: TeamSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamsService(db)
    return service.create_team(response, token, team)


@teams.get("/teams")
async def get_teams(
        response: Response,
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamsService(db)
    return service.list_by_owner(response, token, offset, limit)


@teams.put("/teams")
async def update_team(
        response: Response,
        team_data: TeamUpdateSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamsService(db)
    return service.update(response, token, team_data)
