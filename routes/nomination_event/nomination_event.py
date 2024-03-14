from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.event import EventSchema
from db.schemas.nomination import NominationSchema
from dependencies import authorized_only, get_db
from routes.nomination_event.nomination_event_service import NominationEventService


nomination_event = APIRouter(prefix="/nomination_event", tags=["nomination_event"])


@nomination_event.get("/list_events_list_nominations")
async def list_events_list_nominations(
        response: Response,
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventService(db)
    return service.list(response, token, offset, limit)


@nomination_event.get("/nomination_event_names")
async def get_nominations_events_names(
        response: Response,
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventService(db)
    return service.get_nomination_events_names(response, token, offset, limit)


@nomination_event.get("/nomination_event_full_info")
async def get_nominations_events_full_info(
        response: Response,
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventService(db)
    return service.get_nomination_events_full_info(response, token, offset, limit)


@nomination_event.get('/teams_of_nomination_event')
async def get_teams_of_nomination_event(
        response: Response,
        nomination_name: Annotated[str, Query()],
        event_name: Annotated[str, Query()],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventService(db)
    return service.get_teams_of_nomination_event(response, token, nomination_name, event_name)


@nomination_event.post("/append_nominations_for_event")
async def append_nominations_for_event(
        response: Response,
        event: EventSchema,
        nominations_: list[NominationSchema],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventService(db)
    return service.append_nominations_for_event(response, token, event, nominations_)
