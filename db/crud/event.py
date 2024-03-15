from typing import cast

from sqlalchemy.orm import Session

from db.models.event import Event
from db.crud.nominations import create_nominations_missing_in_db
from db.schemas.event import EventCreateSchema, EventListSchema, EventUpdateSchema
from db.schemas.nomination import NominationSchema


def create_event_db(db: Session, event: EventCreateSchema, owner_id: int) -> type(Event):
    event_db = Event(
        name=event.name,
        date=event.date,
        owner_id=owner_id
    )
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db


def get_all_events_db(db: Session):
    return db.query(Event).all()


def get_events_db(db: Session, offset: int, limit: int) -> list[type(Event)]:
    events_db = db.query(Event).offset(offset).limit(limit).all()
    return events_db


def get_events_with_nominations_db(db: Session, offset: int, limit: int):
    events_db = get_events_db(db, offset, limit)
    return get_events_with_nominations(events_db)


def get_events_with_nominations_by_owner_db(db: Session, offset: int, limit: int, owner_id: int):
    events_db = get_events_by_owner_db(db, offset, limit, owner_id)
    return get_events_with_nominations(events_db)


def get_events_with_nominations(events_db: list[type(Event)]):
    result = []
    for event_db in events_db:
        result.append(
            EventListSchema(
                name=event_db.name,
                date=event_db.date,
                nominations=[
                    NominationSchema.from_orm(nomination_db) for nomination_db in event_db.nominations
                ]
            )
        )
    print(result)
    return result


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


def update_event_db(db: Session, event_data: EventUpdateSchema) -> type(Event):
    event_db = db.query(Event).filter(cast("ColumnElement[bool]", Event.name == event_data.old_name)).first()
    event_db.name = event_data.new_name
    event_db.date = event_data.new_date
    db.add(event_db)
    db.commit()


def get_events_data(events_db: list[type(Event)]):
    events_data = []
    for event_db in events_db:
        events_data.append(EventListSchema.from_orm(event_db))

    return events_data
