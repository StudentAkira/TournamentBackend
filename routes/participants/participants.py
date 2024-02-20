from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from db.schemas import Participant
from dependencies import get_db
from routes.participants.participants_service import ParticipantsService

participants = APIRouter(prefix="/participants", tags=["auth"])


@participants.post("/create")
async def create_participant(token: Annotated[str, Body()], participant: Participant, db: Session = Depends(get_db)) -> dict[str, str]:
    service = ParticipantsService(db)
    return service.create_participant(participant, token)


@participants.get("/get_all_participants")
async def get_all_participants(token: Annotated[str, Body()], db: Session = Depends(get_db)):
    service = ParticipantsService(db)
    return service.get_all_participants(token)
