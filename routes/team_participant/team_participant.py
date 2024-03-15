from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import Response

from dependencies import authorized_only, get_db
from routes.team_participant.team_participant_service import TeamParticipantService

team_participant = APIRouter(prefix="/team_participant", tags=["team_participant"])


@team_participant.post("/team_participant")
async def append_participant_to_team(
        response: Response,
        participant_email: EmailStr,
        team_name: str,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamParticipantService(db)
    return service.append_participant_to_team(response, token, participant_email, team_name)


@team_participant.delete("/team_participant")
async def delete_participant_from_team(
        response: Response,
        participant_email: EmailStr,
        team_name: str,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamParticipantService(db)
    # return service.delete_participant_from_team(response, token, participant_email, team_name)
    return
