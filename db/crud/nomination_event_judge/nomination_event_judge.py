from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.user import User
from db.schemas.nomination_event_judge.get_nomination_event_judge import GetNominationEventJudgeSchema
from db.schemas.nomination_event_judge.nomination_event_judge_data import NominationEventJudgeDataSchema


def create_nomination_event_judge_db(
        db: Session,
        nomination_event_db: type(NominationEvent),
        judge_db: type(User),
):
    nomination_event_db.judges.append(judge_db)
    db.add(nomination_event_db)
    db.commit()


def get_nomination_event_judge_db(
        nomination_event_db: type(NominationEvent),
):
    return nomination_event_db.judges


def delete_nomination_event_judge_db(
        db: Session,
        nomination_event_db: type(NominationEvent),
        judge_db: type(User),
):
    nomination_event_db.judges.remove(judge_db)
    db.add(nomination_event_db)
    db.commit()


def user_in_judge_team_db(nomination_event_db: NominationEvent, user_db: User):
    return user_db in nomination_event_db.judges
