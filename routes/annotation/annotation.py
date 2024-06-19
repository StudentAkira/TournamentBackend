from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.annotation.annotation_create import AnnotationCreateSchema
from db.schemas.annotation.annotation_delete import AnnotationDeleteSchema
from db.schemas.annotation.annotation_get import AnnotationGetSchema
from db.schemas.annotation.annotation_update import AnnotationUpdateSchema
from dependencies.dependencies import get_db, authorized_only
from routes.annotation.annotation_service import AnnotationService

annotation = APIRouter(prefix="/api/annotation", tags=["annotation"])


@annotation.get("/read")
async def read_annotations(
        offset: Annotated[int, Query(gte=0)] = 0,
        limit : Annotated[int, Query(lt=50)] = 49,
        db: Session = Depends(get_db)
) -> list[AnnotationGetSchema]:
    service = AnnotationService(db)
    return service.get_annotations(offset, limit)


@annotation.post("/create")
async def create_annotation(
        response: Response,
        annotation_data:AnnotationCreateSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> dict[str, str]:
    service = AnnotationService(db)
    return service.create_annotation(response, token, annotation_data)


@annotation.patch("/update")
async def update_annotation(
        response: Response,
        annotation_data: AnnotationUpdateSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> dict[str, str]:
    service = AnnotationService(db)
    return service.update_annotation(response, token, annotation_data)


@annotation.delete("/delete")
async def delete_annotation(
        response: Response,
        annotation_data: AnnotationDeleteSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> dict[str, str]:
    service = AnnotationService(db)
    return service.delete_annotation(response, token, annotation_data)
