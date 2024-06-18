from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.participant.participant import ParticipantSchema
from db.schemas.participant.participant_hide import ParticipantHideSchema
from db.schemas.participant.participant_update import ParticipantUpdateSchema
from dependencies.dependencies import get_db, authorized_only
from routes.participant.participants_service import ParticipantsService
from urls import URLs

participants = APIRouter(prefix=URLs.participant_prefix.value, tags=URLs.participant_tags.value)


@participants.get(URLs.participant.value)
async def get_my_participants(
        response: Response,
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipantsService(db)
    return service.list_by_owner(response, token, offset, limit)


@participants.post(URLs.participant.value)
async def create_participant(
        response: Response,
        participant: ParticipantSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipantsService(db)
    return service.create(response, token, participant)


@participants.put(URLs.participant.value)
async def update_participant(
        response: Response,
        participant_data: ParticipantUpdateSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipantsService(db)
    return service.update(response, token, participant_data)


@participants.post("/hide_participant", deprecated=True)
async def hide_participant(
        response: Response,
        participant_data: ParticipantHideSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipantsService(db)
    return service.hide(response, token, participant_data)
