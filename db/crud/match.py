from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.event import Event
from db.models.match import Match
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.team import Team
from db.models.user import User
from db.schemas.group_tournament import GroupMatchSchema
from db.schemas.match import MatchSchema, SetMatchResultSchema
from db.schemas.nomination_event import  OlympycNominationEventSchema, NominationEventType
from db.schemas.team import TeamSchema


def get_group_matches_of_tournament_db(db: Session, nomination_event: OlympycNominationEventSchema):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == nomination_event.event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_event.nomination_name)).first()

    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == NominationEventType.olympyc
        )
    ).first()

    groups = [
        GroupMatchSchema(
            group_id=group_db.id,
            matches=[
                MatchSchema(
                    match_id=match_db.id,
                    team1=TeamSchema(name=match_db.team1.name) if match_db.team1 else None,
                    team2=TeamSchema(name=match_db.team2.name) if match_db.team2 else None,
                    winner=TeamSchema(name=match_db.winner.name) if match_db.winner else None,
                    last_result_creator_email=
                        match_db.last_result_creator.email
                        if match_db.last_result_creator else None,
                    match_queue_number=match_db.match_queue_number
                ) for match_db in group_db.matches
            ]
        ) for group_db in nomination_event_db.groups
    ]
    return groups


def set_match_result_db(db: Session, judge_id: int, data: SetMatchResultSchema):
    match_db = db.query(Match).filter(cast("ColumnElement[bool]", Match.id == data.match_id)).first()
    if data.winner_team_name:
        winner_team_db = db.query(Team).filter(cast("ColumnElement[bool]", Team.name == data.winner_team_name)).first()
        match_db.winner = winner_team_db if winner_team_db else None
    match_db.last_result_creator = db.query(User).filter(cast("ColumnElement[bool]", User.id == judge_id)).first()
    db.add(match_db)
    db.commit()


def is_match_related_to_nomination_event_db(db: Session, data: SetMatchResultSchema):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == data.nomination_event.event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == data.nomination_event.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == NominationEventType.olympyc
        )
    ).first()

    match = db.query(Match).filter(cast("ColumnElement[bool]", Match.id == data.match_id)).first()
    for group in nomination_event_db.groups:
        if match in group.matches:
            return True
    return False
