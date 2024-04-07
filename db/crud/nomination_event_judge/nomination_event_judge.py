from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.user import User
from db.schemas.nomination_event_judge.get_nomination_event_judge import GenNominationEventJudgeSchema
from db.schemas.nomination_event_judge.nomination_event_judge_data import NominationEventJudgeDataSchema


def create_nomination_event_judge_db(db: Session, data: NominationEventJudgeDataSchema):
    event_db = db.query(Event).filter(cast("ColumnElement[bool]", Event.name == data.event_name)).first()
    nomination_db = db.query(Nomination).filter(cast("ColumnElement[bool]", Nomination.name == data.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == data.nomination_event_type
        )
    ).first()
    judge = db.query(User).filter(cast("ColumnElement[bool]", User.email == data.email)).first()
    nomination_event_db.judges.append(judge)
    db.add(nomination_event_db)
    db.commit()


def get_nomination_event_judge_db(db: Session, data: GenNominationEventJudgeSchema):
    event_db = db.query(Event).filter(cast("ColumnElement[bool]", Event.name == data.event_name)).first()
    nomination_db = db.query(Nomination).filter(cast("ColumnElement[bool]", Nomination.name == data.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == data.nomination_event_type
        )
    ).first()
    return nomination_event_db.judges


def delete_nomination_event_judge_db(db: Session, data: NominationEventJudgeDataSchema):
    event_db = db.query(Event).filter(cast("ColumnElement[bool]", Event.name == data.event_name)).first()
    nomination_db = db.query(Nomination).filter(cast("ColumnElement[bool]", Nomination.name == data.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == data.nomination_event_type
        )
    ).first()
    judge = db.query(User).filter(cast("ColumnElement[bool]", User.email == data.email)).first()

    nomination_event_db.judges.remove(judge)
    db.add(nomination_event_db)
    db.commit()
