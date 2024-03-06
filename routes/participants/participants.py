from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.participant import ParticipantSchema
from db.schemas.team import TeamSchema
from dependencies import get_db, authorized_only
from routes.participants.participants_service import ParticipantsService

participants = APIRouter(prefix="/participants", tags=["participants"])


@participants.get("/participant")
async def get_my_participants(
        response: Response,
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipantsService(db)
    return service.get_participants_by_owner(response, token, offset, limit)


@participants.post("/participant")
async def create_participant(
        response: Response,
        participant: ParticipantSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipantsService(db)
    return service.create_participant(response, token, participant)


@participants.post("/participant_to_team")
async def append_participant_to_team(
        response: Response,
        participant_email: EmailStr,
        team_name: str,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipantsService(db)
    return service.append_participant_to_team(response, token, participant_email, team_name)
