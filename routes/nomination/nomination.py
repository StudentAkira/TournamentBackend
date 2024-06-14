from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination.nomination import NominationSchema
from dependencies import get_db, authorized_only
from routes.nomination.nomination_service import NominationsService
from urls import URLs

nominations = APIRouter(prefix=URLs.nomination_prefix.value, tags=URLs.nomination_tags.value)


@nominations.get(URLs.nomination.value)
async def get_nominations(
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        db: Session = Depends(get_db)
):
    service = NominationsService(db)
    return service.list(offset, limit)


@nominations.get(URLs.get_nominations_related_to_event.value)
async def get_nominations_related_to_event(
        event_id: Annotated[int, Query()],
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        db: Session = Depends(get_db)
):
    service = NominationsService(db)
    return service.get_nominations_related_to_event(event_id, offset, limit)


@nominations.get(URLs.get_nominations_not_related_to_event.value)
async def get_nominations_not_related_to_event(
        event_id: Annotated[int, Query()],
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        db: Session = Depends(get_db)
):
    service = NominationsService(db)
    return service.get_nominations_not_related_to_event(event_id, offset, limit)


@nominations.post(URLs.nomination.value)
async def create_nomination(
        response: Response,
        nomination: NominationSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationsService(db)
    return service.create(response, token, nomination)


@nominations.put(URLs.nomination.value)
async def update_nomination(
        response: Response,
        old_nomination: NominationSchema,
        new_nomination: NominationSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationsService(db)
    return service.update(response, token, old_nomination, new_nomination)
