from typing import cast

from sqlalchemy import exists
from sqlalchemy.orm import Session

from db.crud.general import create_missing_items
from db.models.nomination import Nomination
from db.schemas.nomination.nomination import NominationSchema


def create_nomination_db(db: Session, nomination: NominationSchema):
    nomination_db = Nomination(
        name=nomination.name
    )
    db.add(nomination_db)
    db.commit()


def create_nominations_missing_in_db(db: Session, nominations: list[NominationSchema] | None) -> list[type(Nomination)]:
    nominations_db = create_missing_items(db, Nomination, nominations)
    return nominations_db


def save_nominations_db(db: Session, nominations: list[NominationSchema]) -> list[type(Nomination)]:
    nominations_db = create_nominations_missing_in_db(db, nominations)
    db.commit()
    return nominations_db


def get_all_nominations_db(db: Session):
    return db.query(Nomination).all()


def get_nominations_by_names_db(db: Session, names: set[str]) -> list[type(Nomination)]:
    nominations_db = db.query(Nomination).filter(
        Nomination.name.in_(names)
    ).all()
    return nominations_db


def get_nominations_db(db: Session, offset: int, limit: int) -> list[type(Nomination)]:
    nominations_db = db.query(Nomination).offset(offset).limit(limit).all()
    return nominations_db


def get_nomination_by_name_db(db: Session, name: str) -> type(Nomination):
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == name)
    ).first()
    return nomination_db


def nomination_exists_db(db: Session, nomination_name: str):
    entity_exists = db.query(exists().where(cast("ColumnElement[bool]", Nomination.name == nomination_name))).scalar()
    return entity_exists


def update_nomination_db(db: Session, old_nomination: NominationSchema, new_nomination: NominationSchema):
    nomination_db = db.query(Nomination).\
        filter(cast("ColumnElement[bool]", Nomination.name == old_nomination.name)).first()
    nomination_db.name = new_nomination.name
    db.add(nomination_db)
    db.commit()


def delete_nomination_db(db: Session, nomination_name: str):
    pass

