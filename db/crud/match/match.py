from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.event import Event
from db.models.match import Match
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.team import Team
from db.models.user import User
from db.schemas.bracket.bracket_tournament import BracketMatchesSchema
from db.schemas.group_tournament.group_matches import GroupMatchesSchema
from db.schemas.match.bracket_match_schema import BracketMatchSchema
from db.schemas.match.group_match_schema import GroupMatchSchema
from db.schemas.match.set_match_result_schema import SetMatchResultSchema
from db.schemas.nomination_event.nomination_event_type import NominationEventType
from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema
from db.schemas.team.team import TeamSchema


def get_group_matches_db(db: Session, nomination_event: OlympycNominationEventSchema):
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
        GroupMatchesSchema(
            group_id=group_db.id,
            matches=[
                GroupMatchSchema(
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


def get_bracket_matches_db(db: Session, nomination_event: OlympycNominationEventSchema):
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

    result = BracketMatchesSchema(matches=[BracketMatchSchema(
        match_id=match.id,
        team1=TeamSchema.from_orm(match.team1) if match.team1 else None,
        team2=TeamSchema.from_orm(match.team2) if match.team2 else None,
        winner=TeamSchema.from_orm(match.winner) if match.winner else None,
        last_result_creator_email=match.last_result_creator.email if match.last_result_creator else None,
        next_match_id=match.next_bracket_match_id
    ) for match in nomination_event_db.bracket.matches])

    return result


def set_group_match_result_db(db: Session, judge_id: int, data: SetMatchResultSchema):
    match_db = db.query(Match).filter(cast("ColumnElement[bool]", Match.id == data.match_id)).first()
    if data.winner_team_name:
        winner_team_db = db.query(Team).filter(cast("ColumnElement[bool]", Team.name == data.winner_team_name)).first()
        match_db.winner = winner_team_db if winner_team_db else None
    match_db.last_result_creator = db.query(User).filter(cast("ColumnElement[bool]", User.id == judge_id)).first()
    db.add(match_db)
    db.commit()


def set_bracket_match_result_db(db: Session, judge_id: int, data: SetMatchResultSchema):
    match_db = db.query(Match).filter(cast("ColumnElement[bool]", Match.id == data.match_id)).first()
    winner_team_db = db.query(Team).filter(cast("ColumnElement[bool]", Team.name == data.winner_team_name)).first()
    if match_db.winner == winner_team_db:
        return
    match_db.winner = winner_team_db
    match_db.last_result_creator = db.query(User).filter(cast("ColumnElement[bool]", User.id == judge_id)).first()
    defeated_team = match_db.team1 if match_db.team1 != winner_team_db else match_db.team2

    db.add(match_db)

    match_db = match_db.next_bracket_match

    if match_db is None:
        db.commit()
        return

    match_db.team1 = None if match_db.team1 == defeated_team else match_db.team1
    match_db.team2 = None if match_db.team2 == defeated_team else match_db.team2
    if match_db.team1 is None:
        match_db.team1 = winner_team_db
    elif match_db.team2 is None:
        match_db.team2 = winner_team_db

    while match_db:
        match_db.team1 = None if match_db.team1 == defeated_team else match_db.team1
        match_db.team2 = None if match_db.team2 == defeated_team else match_db.team2

        match_db.winner = None
        match_db.last_result_creator = None
        db.add(match_db)
        match_db = match_db.next_bracket_match
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
    if match in nomination_event_db.bracket.matches:
        return True
    return False


def is_winner_exists_in_bracket_match_db(db: Session, data: SetMatchResultSchema):
    match_in_bracket = db.query(Match).filter(cast("ColumnElement[bool]", Match.id == data.match_id)).first()
    if data.winner_team_name is None and match_in_bracket.bracket is not None:
        return False
    return True


def is_prev_match_was_judged_db(db: Session, data: SetMatchResultSchema):
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

    prev_matches = [
        match for match in nomination_event_db.bracket.matches if match.next_bracket_match_id == data.match_id
    ]

    # print(len(prev_matches))
    # print(prev_matches[0].id, prev_matches[1].id)
    # print(prev_matches[0].last_result_creator, prev_matches[1].last_result_creator)

    if len(prev_matches) == 0:
        return True
    if prev_matches[0].last_result_creator is None:
        return False
    if prev_matches[1].last_result_creator is None:
        return False
    return True
