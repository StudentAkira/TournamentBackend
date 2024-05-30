from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.event.event import EventSchema
from db.schemas.event.event_create import EventCreateSchema
from db.schemas.event.event_delete import EventDeleteSchema
from db.schemas.event.event_update import EventUpdateSchema
from dependencies import get_db, authorized_only
from routes.event.events_service import EventsService

events = APIRouter(prefix="/api/event", tags=["event"])


@events.get("/event")
async def get_events_by_owner(
        response: Response,
        offset: Annotated[int, Query(gte=0)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 49,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> list[EventSchema]:
    service = EventsService(db)
    return service.list_by_owner(response, token, offset, limit)


@events.get("/events_with_nominations")
async def get_events_with_nominations(
    response: Response,
        offset: Annotated[int, Query(gte=0)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 49,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = EventsService(db)
    return service.list_with_nominations(response, token, offset, limit)


@events.post("/event")
async def create_event(
        response: Response,
        event: EventCreateSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> dict[str, str]:
    service = EventsService(db)
    return service.create(response, token, event)


@events.put("/event")
async def update_event(
        response: Response,
        event_data: EventUpdateSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> dict[str, str]:
    service = EventsService(db)
    return service.update(response, token, event_data)


@events.delete("/event")
async def delete_event(
        response: Response,
        event_data: EventDeleteSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> dict[str, str]:
    service = EventsService(db)
    return service.delete(response, token, event_data)
