from typing import cast

from sqlalchemy.orm import Session

from db import models


def get_nomination_event_db(
        db: Session,
        nomination_name: str,
        event_name: str,
) -> type(models.NominationEvent) | None:
    event_db = db.query(models.Event).filter(
        cast("ColumnElement[bool]", models.Event.name == event_name)
    ).first()
    nomination_db = db.query(models.Nomination).filter(
        cast("ColumnElement[bool]", models.Nomination.name == nomination_name)
    ).first()
    nomination_event_db = db.query(models.NominationEvent) \
        .filter(models.NominationEvent.event_id == event_db.id
                and models.NominationEvent.nomination_id == nomination_db.id).first()
    return nomination_event_db


def get_nomination_events_db(
        db: Session,
        offset: int,
        limit: int
) -> list[type(models.NominationEvent)]:
    nominations_events_db = db.query(models.NominationEvent).offset(offset).limit(limit).all()
    return nominations_events_db


def get_nomination_events_by_owner_db(
        db: Session,
        offset: int,
        limit: int,
        owner_id: int
) -> list[type(models.NominationEvent)]:
    events_db = db.query(models.Event).filter(cast("ColumnElement[bool]", models.Event.owner_id == owner_id)).all()
    events_ids = {event_db.id for event_db in events_db}
    nominations_events_db = db.query(models.NominationEvent). \
        filter(models.NominationEvent.event_id.in_(events_ids)). \
        offset(offset).limit(limit).all()
    return nominations_events_db
