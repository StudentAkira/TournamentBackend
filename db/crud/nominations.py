from typing import cast

from sqlalchemy.orm import Session

from db import models
from db.crud.general import create_missing_items
from db.schemas.nomination import NominationSchema


def create_nominations_missing_in_db(db: Session, nominations: list[NominationSchema]) -> list[type(models.Nomination)]:
    nominations_db = create_missing_items(db, models.Nomination, nominations)
    return nominations_db


def save_nominations_db(db: Session, nominations: list[NominationSchema]) -> list[type(models.Nomination)]:
    nominations_db = create_nominations_missing_in_db(db, nominations)
    db.commit()
    return nominations_db


def get_nominations_by_names_db(db: Session, names: set[str]) -> list[type(models.Nomination)]:
    nominations_db = db.query(models.Nomination).filter(
        models.Nomination.name.in_(names)
    ).all()
    return nominations_db


def get_nominations_db(db: Session, offset: int, limit: int) -> list[type(models.Nomination)]:
    nominations_db = db.query(models.Nomination).offset(offset).limit(limit).all()
    nominations = [NominationSchema.from_orm(nomination) for nomination in nominations_db]
    return nominations_db


def get_nomination_by_name_db(db: Session, name: str) -> type(models.Nomination):
    nomination_db = db.query(models.Nomination).filter(
        cast("ColumnElement[bool]", models.Nomination.name == name)
    ).first()
    return nomination_db
