from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.event.event import EventSchema
from db.schemas.event.event_by_id import EventByIdSchema
from db.schemas.event.event_create import EventCreateSchema
from db.schemas.event.event_delete import EventDeleteSchema
from db.schemas.event.event_update import EventUpdateSchema
from dependencies import get_db, authorized_only
from routes.event.events_service import EventsService
from urls import URLs

events = APIRouter(prefix=URLs.event_prefix.value, tags=URLs.event.event_tags.value)


@events.get(URLs.get_event_by_id.value)
async def get_event_by_id(
        response: Response,
        event_id: Annotated[int, Query()],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> EventByIdSchema:
    service = EventsService(db)
    return service.get_by_id(response, token, event_id)


@events.get(URLs.event.value)
async def get_events_by_owner(
        response: Response,
        offset: Annotated[int, Query(gte=0)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 49,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> list[EventSchema]:
    service = EventsService(db)
    return service.list_by_owner(response, token, offset, limit)


@events.get(URLs.get_event_with_nominations.value)
async def get_events_with_nominations(
    response: Response,
        offset: Annotated[int, Query(gte=0)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 49,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = EventsService(db)
    return service.list_with_nominations(response, token, offset, limit)


@events.post(URLs.event.value)
async def create_event(
        response: Response,
        event: EventCreateSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> dict[str, str]:
    service = EventsService(db)
    return service.create(response, token, event)


@events.put(URLs.event.value)
async def update_event(
        response: Response,
        event_data: EventUpdateSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> dict[str, str]:
    service = EventsService(db)
    return service.update(response, token, event_data)


@events.delete(URLs.event.value)
async def delete_event(
        response: Response,
        event_data: EventDeleteSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> dict[str, str]:
    service = EventsService(db)
    return service.delete(response, token, event_data)
