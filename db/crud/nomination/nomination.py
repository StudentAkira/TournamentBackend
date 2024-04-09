from typing import cast
from sqlalchemy.orm import Session
from db.models.nomination import Nomination
from db.schemas.nomination.nomination import NominationSchema


def create_nomination_db(db: Session, nomination: NominationSchema):
    nomination_db = Nomination(
        name=nomination.name
    )
    db.add(nomination_db)
    db.commit()


def get_all_nominations_db(db: Session):
    return db.query(Nomination).all()


def get_nominations_db(db: Session, offset: int, limit: int) -> list[type(Nomination)]:
    nominations_db = db.query(Nomination).offset(offset).limit(limit).all()
    return nominations_db


def get_nomination_by_name_db(db: Session, name: str) -> type(Nomination):
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == name)
    ).first()
    return nomination_db


def update_nomination_db(db: Session, nomination_db: type(Nomination), new_nomination: NominationSchema):
    nomination_db.name = new_nomination.name
    db.add(nomination_db)
    db.commit()
