from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.equipment import EquipmentSchema
from dependencies import get_db, authorized_only
from routes.equipment.equipment_service import EquipmentService

equipment = APIRouter(prefix="/equipment", tags=["equipment"])


@equipment.get("/equipment")
async def get_equipment(
        response: Response,
        offset: Annotated[int, Query(gte=0, lt=50)],
        limit: Annotated[int, Query(lt=50, gt=0)],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> list[EquipmentSchema]:
    service = EquipmentService(db)
    return service.get_equipment(response, offset, limit, token)


@equipment.post("/equipment")
async def create_equipment(
        response: Response,
        equipment_: list[EquipmentSchema],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> dict[str, str]:
    service = EquipmentService(db)
    return service.create_equipment(response, token, equipment_)
