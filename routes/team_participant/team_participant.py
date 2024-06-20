from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.team_participant.team_participant_append import TeamParticipantAppendSchema
from dependencies.dependencies import authorized_only, get_db
from routes.team_participant.team_participant_service import TeamParticipantService
from urls import URLs

team_participant = APIRouter(prefix=URLs.team_participant_prefix.value, tags=URLs.team_participant_tags.value)


@team_participant.post(URLs.team_participant.value)
async def append_participant_to_team(
        response: Response,
        team_participant_data: TeamParticipantAppendSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamParticipantService(db)
    return service.append_participant_to_team(response, token, team_participant_data)
