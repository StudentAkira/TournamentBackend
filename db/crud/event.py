from typing import cast

from sqlalchemy.orm import Session

from db import models
from db.crud.nominations import create_nominations_missing_in_db
from db.schemas.event import EventSchema, EventCreateSchema
from db.schemas.nomination import NominationSchema


def create_event_db(db: Session, event: EventCreateSchema, owner_id: int) -> type(models.Event):
    nominations = event.nominations
    nominations_db = create_nominations_missing_in_db(db, nominations)
    event_db = models.Event(
        name=event.name,
        owner_id=owner_id
    )
    event_db.nominations.extend(nominations_db)
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db


def get_all_events_db(db: Session):
    return db.query(models.Event).all()


def get_events_db(db: Session, offset: int, limit: int) -> list[type(models.Event)]:
    events_db = db.query(models.Event).offset(offset).limit(limit).all()
    return events_db


def get_event_by_name_db(db: Session, name: str) -> type(models.Event) | None:
    event_db = db.query(models.Event).filter(
        cast("ColumnElement[bool]", models.Event.name == name)
    ).first()
    return event_db


def get_events_by_owner_db(db: Session, offset: int, limit: int, owner_id: int) -> list[type(models.Event)]:
    events_db = db.query(models.Event).filter(
        cast("ColumnElement[bool]", models.Event.owner_id == owner_id)
    ).offset(offset).limit(limit).all()
    return events_db


def append_event_nominations_db(
        db: Session,
        event: EventSchema,
        nominations: list[NominationSchema]
) -> type(models.Event):
    nominations_db = create_nominations_missing_in_db(db, nominations)
    event_db = get_event_by_name_db(db, event.name)
    event_db.nominations.extend(set(nominations_db) - set(event_db.nominations))
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db
