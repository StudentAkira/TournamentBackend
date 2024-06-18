from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.annotations import Annotation
from db.schemas.annotation.annotation_create import AnnotationCreateSchema
from db.schemas.annotation.annotation_update import AnnotationUpdateSchema


def get_annotations_db(db: Session, offset: int, limit: int) -> list[type(Annotation)]:
    annotations_db = db.query(Annotation).offset(offset).limit(limit).all()
    return annotations_db


def get_annotation_by_name_db(db: Session, text: str) -> Annotation | None:
    annotation_db = db.query(Annotation).filter(cast("ColumnElement[bool]", Annotation.text == text)).first()
    return annotation_db


def get_annotation_by_id_db(db: Session, annotation_id: int, user_id: int) -> Annotation | None:
    annotation_db = db.query(Annotation).filter(
        and_(
            cast("ColumnElement[bool]", Annotation.id == annotation_id),
            cast("ColumnElement[bool]", Annotation.owner_id == user_id),
        )
    ).first()
    return annotation_db


def create_annotation_db(db: Session, user_id: int, annotation_data: AnnotationCreateSchema):
    annotation_db = Annotation(
        owner_id=user_id,
        text=annotation_data.text
    )
    db.add(annotation_db)
    db.commit()


def update_annotation_db(db: Session, annotation_db: Annotation, annotation_data: AnnotationUpdateSchema):
    annotation_db.text = annotation_data.new_text
    db.add(annotation_db)
    db.commit()


def delete_annotation_db(db: Session, annotation_db: Annotation):
    db.delete(annotation_db)
    db.commit()
