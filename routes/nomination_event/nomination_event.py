from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event.nomination_event import NominationEventSchema
from db.schemas.nomination_event.nomination_event_delete import NominationEventDeleteSchema
from dependencies import authorized_only, get_db
from routes.nomination_event.nomination_event_service import NominationEventService


nomination_event = APIRouter(prefix="/api/nomination_event", tags=["nomination_event"])


@nomination_event.post("/nomination_event_pdf")
async def get_event_pdf(
    response: Response,
    data: list[NominationEventSchema],
    token: str = Depends(authorized_only),
    db: Session = Depends(get_db)
):
    service = NominationEventService(db)
    out = service.get_nomination_event_pdf(response, token, data)
    headers = {'Content-Disposition': 'attachment; filename="out.pdf"'}
    return Response(bytes(out), headers=headers, media_type='application/pdf')


@nomination_event.get("/nomination_event_data")
async def get_nomination_event_data(
    response: Response,
    event_name: Annotated[str, Query()],
    token: str = Depends(authorized_only),
    db: Session = Depends(get_db)
):
    service = NominationEventService(db)
    return service.get_nomination_event_data(response, token, event_name)


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


@nomination_event.post("/append_nomination_for_event")
async def append_nomination_for_event(
        response: Response,
        nomination_event_data: NominationEventSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventService(db)
    return service.append_nomination_for_event(response, token, nomination_event_data)


@nomination_event.delete("/delete_nomination_from_event")
async def delete_nomination_from_event(
    response: Response,
    nomination_event_data: NominationEventDeleteSchema,
    token: str = Depends(authorized_only),
    db: Session = Depends(get_db)
):
    service = NominationEventService(db)
    return service.delete(response, token, nomination_event_data)


@nomination_event.post("/close_registration")
async def close_registration(
        response: Response,
        nomination_event_data: NominationEventSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventService(db)
    return service.close_registration(response, token, nomination_event_data)


@nomination_event.post("/open_registration")
async def open_registration(
        response: Response,
        nomination_event_data: NominationEventSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationEventService(db)
    return service.open_registration(response, token, nomination_event_data)
