from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.annotation.annotation import get_annotation_by_name_db, create_annotation_db, get_annotation_by_id_db, \
    update_annotation_db, delete_annotation_db
from db.models.annotations import Annotation
from db.schemas.annotation.annotation_create import AnnotationCreateSchema
from db.schemas.annotation.annotation_update import AnnotationUpdateSchema


class AnnotationManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__annotation_name_taken_error = "annotation name taken"
        self.__annotation_not_found_error = "annotation not found"

    def get_by_id_and_user_id(self, annotation_id: int, user_id: int) -> Annotation:
        annotation_db = get_annotation_by_id_db(self.__db, annotation_id, user_id)
        return annotation_db

    def get_by_text(self, text: str) -> Annotation:
        annotation_db = get_annotation_by_name_db(self.__db, text)
        return annotation_db

    def create(self, user_id: int, annotation_data: AnnotationCreateSchema):
        create_annotation_db(self.__db, user_id, annotation_data)

    def update(self, annotation_db: Annotation, annotation_data: AnnotationUpdateSchema):
        update_annotation_db(self.__db, annotation_db, annotation_data)

    def delete(self, annotation_db: Annotation):
        delete_annotation_db(self.__db, annotation_db)

    def raise_exception_if_text_taken(self, annotation_db: Annotation | None):
        if annotation_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__annotation_name_taken_error}
            )

    def raise_exception_if_not_found(self, annotation_db: Annotation | None):
        if annotation_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__annotation_not_found_error}
            )


