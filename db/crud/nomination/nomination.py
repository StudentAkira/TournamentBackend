from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.event import Event
from db.models.nomination import Nomination
from db.schemas.nomination.nomination_create import NominationCreateSchema
from db.schemas.nomination.nomination_update import NominationUpdateSchema


def create_nomination_db(db: Session, user_id: int, nomination: NominationCreateSchema):
    nomination_db = Nomination(
        name=nomination.name,
        owner_id=user_id
    )
    db.add(nomination_db)
    db.commit()


def get_all_nominations_db(db: Session):
    return db.query(Nomination).all()


def get_nominations_db(db: Session, user_id: int, offset: int, limit: int) -> list[type(Nomination)]:
    nominations_db = db.query(Nomination).\
        filter(
        cast("ColumnElement[bool]", Nomination.owner_id == user_id)
    ).offset(offset).limit(limit).all()
    return nominations_db


def get_event_related_nominations(db: Session, event_db: Event, offset: int, limit: int) -> list[type(Nomination)]:
    nominations_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]",
             Nomination.id.in_(
                        set([nomination_db.id for nomination_db in event_db.nominations])
                    )
            )
    ).offset(offset).limit(limit).all()
    return nominations_db


def get_event_not_related_nominations(db: Session, event_db: Event, offset: int, limit: int) -> list[type(Nomination)]:
    nominations_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]",
             Nomination.id.notin_(
                        set([nomination_db.id for nomination_db in event_db.nominations])
                    )
            )
    ).offset(offset).limit(limit).all()
    return nominations_db


def get_event_related_nominations_starts_with(
        db: Session,
        event_db: Event,
        title: str,
        offset: int,
        limit: int
) -> list[type(Nomination)]:
    nominations_db = db.query(Nomination).filter(
        and_(
             Nomination.id.in_(
                 set([nomination_db.id for nomination_db in event_db.nominations])
                ),
            Nomination.name.ilike(f"%{title}%")
        )
    ).offset(offset).limit(limit).all()
    return nominations_db


def get_event_not_related_nominations_starts_with(
        db: Session,
        event_db: Event,
        title: str,
        offset: int,
        limit: int
) -> list[type(Nomination)]:
    nominations_db = db.query(Nomination).filter(
        and_(
             Nomination.id.notin_(
                 set([nomination_db.id for nomination_db in event_db.nominations])
                ),
             Nomination.name.ilike(f"%{title}%")
        )
    ).offset(offset).limit(limit).all()
    return nominations_db


def get_nomination_by_name_and_user_id_db(db: Session, user_id: int, name: str) -> type(Nomination):
    nomination_db = db.query(Nomination).filter(
        and_(
            Nomination.name == name,
            Nomination.owner_id == user_id
        )
    ).first()
    return nomination_db


def update_nomination_db(db: Session, nomination_db: type(Nomination), nomination_data: NominationUpdateSchema):
    nomination_db.name = nomination_data.new_name
    db.add(nomination_db)
    db.commit()


def get_nomination_by_id_and_user_id_db(db: Session, user_id: int, nomination_id: int) -> Nomination | None:
    nomination_db = db.query(Nomination).filter(
        and_(
            Nomination.id == nomination_id,
            Nomination.owner_id == user_id
        )
    ).first()
    return nomination_db
