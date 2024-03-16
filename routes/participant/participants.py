from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.participant import ParticipantSchema, ParticipantHideSchema
from dependencies import get_db, authorized_only
from routes.participant.participants_service import ParticipantsService

participants = APIRouter(prefix="/participant", tags=["participant"])


@participants.get("/participant")
async def get_my_participants(
        response: Response,
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipantsService(db)
    return service.list_by_owner(response, token, offset, limit)


@participants.post("/participant")
async def create_participant(
        response: Response,
        participant: ParticipantSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipantsService(db)
    return service.create(response, token, participant)


@participants.put("/participant")
async def update_participant(
        response: Response,
        participant: ParticipantSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipantsService(db)
    # return service.update(response, token, participant)
    return


@participants.post("/hide_participant")
async def hide_participant(
        response: Response,
        participant_data: ParticipantHideSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipantsService(db)
    return service.hide(response, token, participant_data)
