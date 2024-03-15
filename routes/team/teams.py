from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.team import TeamSchema, TeamUpdateSchema
from dependencies import get_db, authorized_only
from routes.team.teams_service import TeamsService

teams = APIRouter(prefix="/team", tags=["team"])


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



# @team.post("/team_software_equipment")
# async def set_team_software_and_equipment_in_event_nomination(
#         response: Response,
#         team_name: Annotated[str, Body()],
#         event_name: Annotated[str, Body()],
#         nomination_name: Annotated[str, Body()],
#         software: Annotated[str, Body()],
#         equipment: Annotated[str, Body()],
#         token: str = Depends(authorized_only),
#         db: Session = Depends(get_db)
# ):
#     service = TeamsService(db)
#     return service.set_team_software_and_equipment_in_event_nomination(
#         response,
#         token,
#         team_name,
#         nomination_name,
#         event_name,
#         software,
#         equipment
#     )
