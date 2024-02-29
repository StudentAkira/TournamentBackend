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
