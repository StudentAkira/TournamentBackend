from typing import Annotated

from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination import NominationSchema
from dependencies import get_db, authorized_only
from routes.nomination.nominations_service import NominationsService

nominations = APIRouter(prefix="/nomination", tags=["nomination"])


@nominations.get("/nominations")
async def get_nominations(
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        db: Session = Depends(get_db)
):
    service = NominationsService(db)
    return service.list(offset, limit)


@nominations.post("/nominations")
async def create_nominations(
        response: Response,
        nominations_: list[NominationSchema],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationsService(db)
    return service.create_many(response, token, nominations_)


@nominations.put("/nomination")
async def update_nomination(
        response: Response,
        old_nomination: NominationSchema,
        new_nomination: NominationSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = NominationsService(db)
    return service.update(response, token, old_nomination, new_nomination)
