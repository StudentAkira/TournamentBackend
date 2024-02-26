from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.software import SoftwareSchema
from dependencies import get_db, authorized_only
from routes.software.software_service import SoftwareService

software = APIRouter(prefix="/software", tags=["software"])


@software.post("/software")
async def create_software(
        response: Response,
        software_: list[SoftwareSchema],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = SoftwareService(db)
    return service.create_software(response, token, software_)


@software.get("/software")
async def get_software(
        response: Response,
        offset: Annotated[int, Query(gte=0, lt=50)] = 0,
        limit: Annotated[int, Query(lt=50, gt=0)] = 10,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = SoftwareService(db)
    return service.get_software(response, offset, limit, token)
