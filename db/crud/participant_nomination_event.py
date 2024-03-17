from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.participant import Participant


def get_participants_of_nomination_event_db(db: Session, nomination_name: str, event_name: str):
    event_db = db.query(Event).filter(cast("ColumnElement[bool]", Event.name == event_name)).first()
    nomination_db = db.query(Nomination).filter(cast("ColumnElement[bool]", Nomination.name == nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id
        )
    ).first()
    participants_ids = set(participant_db.participant_id for participant_db in nomination_event_db.team_participants)
    participants_db = db.query(Participant).filter(Participant.id.in_(participants_ids))
    return participants_db
