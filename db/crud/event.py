from typing import cast

from sqlalchemy.orm import Session

from db.models.event import Event
from db.crud.nominations import create_nominations_missing_in_db
from db.schemas.event import EventSchema, EventCreateSchema, EventListSchema
from db.schemas.nomination import NominationSchema


def create_event_db(db: Session, event: EventCreateSchema, owner_id: int) -> type(Event):
    nominations = event.nominations
    nominations_db = create_nominations_missing_in_db(db, nominations)
    event_db = Event(
        name=event.name,
        date=event.date,
        owner_id=owner_id
    )
    event_db.nominations.extend(nominations_db)
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db


def get_all_events_db(db: Session):
    return db.query(Event).all()


def get_events_db(db: Session, offset: int, limit: int) -> list[type(Event)]:
    events_db = db.query(Event).offset(offset).limit(limit).all()
    return events_db


def get_event_by_name_db(db: Session, name: str) -> type(Event) | None:
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == name)
    ).first()
    return event_db


def get_events_by_owner_db(db: Session, offset: int, limit: int, owner_id: int) -> list[type(Event)]:
    events_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.owner_id == owner_id)
    ).offset(offset).limit(limit).all()
    return events_db


def get_all_events_by_owner_db(db: Session, owner_id: int) -> list[type(Event)]:
    events_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.owner_id == owner_id)
    ).all()
    return events_db


def append_event_nominations_db(
        db: Session,
        event: EventSchema,
        nominations: list[NominationSchema]
) -> type(Event):
    nominations_db = create_nominations_missing_in_db(db, nominations)
    event_db = get_event_by_name_db(db, event.name)
    event_db.nominations.extend(set(nominations_db) - set(event_db.nominations))
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db


def update_event_db(db: Session, old_event: EventCreateSchema, new_event: EventCreateSchema,) -> type(Event):
    event_db = db.query(Event).filter(cast("ColumnElement[bool]", Event.name == old_event.name)).first()
    event_db.name = new_event.name
    event_db.date = new_event.date
    db.add(event_db)
    db.commit()


def get_events_data(events_db: list[type(Event)]):
    events_data = []
    for event_db in events_db:
        events_data.append(EventListSchema.from_orm(event_db))
    return events_data
