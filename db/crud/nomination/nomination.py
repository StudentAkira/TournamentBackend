from typing import cast

from sqlalchemy import and_, not_
from sqlalchemy.orm import Session

from db.models.event import Event
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


def get_nomination_by_name_db(db: Session, name: str) -> type(Nomination):
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == name)
    ).first()
    return nomination_db


def update_nomination_db(db: Session, nomination_db: type(Nomination), new_nomination: NominationSchema):
    nomination_db.name = new_nomination.name
    db.add(nomination_db)
    db.commit()
