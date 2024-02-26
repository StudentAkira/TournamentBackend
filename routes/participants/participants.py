from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.participant import ParticipantSchema
from dependencies import get_db, authorized_only
from routes.participants.participants_service import ParticipantsService

participants = APIRouter(prefix="/participants", tags=["participants"])


@participants.get("/participant")
async def get_my_participants(
        response: Response,
        offset: int,
        limit: int,
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
