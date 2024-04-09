from typing import cast

from sqlalchemy.orm import Session

from db.models.match import Match
from db.models.nomination_event import NominationEvent
from db.models.team import Team
from db.models.user import User
from db.schemas.bracket.bracket_tournament import BracketMatchesSchema
from db.schemas.group_tournament.group_matches import GroupMatchesSchema
from db.schemas.match.bracket_match_schema import BracketMatchSchema
from db.schemas.match.group_match_schema import GroupMatchSchema
from db.schemas.match.set_match_result_schema import SetMatchResultSchema
from db.schemas.team.team import TeamSchema


def get_match_by_id(db: Session, match_id: int):
    match_db = db.query(Match).filter(cast("ColumnElement[bool]", Match.id == match_id)).first()
    return match_db


def get_group_matches_db(nomination_event_db: type(NominationEvent)):
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


def get_bracket_matches_db(nomination_event_db: type(NominationEvent)):
    result = BracketMatchesSchema(matches=[BracketMatchSchema(
        match_id=match.id,
        team1=TeamSchema.from_orm(match.team1) if match.team1 else None,
        team2=TeamSchema.from_orm(match.team2) if match.team2 else None,
        winner=TeamSchema.from_orm(match.winner) if match.winner else None,
        last_result_creator_email=match.last_result_creator.email if match.last_result_creator else None,
        next_match_id=match.next_bracket_match_id
    ) for match in nomination_event_db.bracket.matches])

    return result


def set_group_match_result_db(db: Session, judge_db: type(User), match_db: type(Match), team_db: type(Team)):
    if team_db:
        match_db.winner = team_db
    match_db.last_result_creator = judge_db
    db.add(match_db)
    db.commit()


def set_bracket_match_result_db(db: Session, judge_db: type(User), match_db: type(Match), winner_team_db: type(Team)):
    if match_db.winner == winner_team_db:
        return
    match_db.winner = winner_team_db
    match_db.last_result_creator = judge_db
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


def is_match_related_to_nomination_event_db(
        nomination_event_db: type(NominationEvent),
        match_db: type(Match)
):
    for group in nomination_event_db.groups:
        if match_db in group.matches:
            return True
    if match_db in nomination_event_db.bracket.matches:
        return True
    return False


def is_prev_match_was_judged_db(nomination_event_db: type(NominationEvent), match_db: type(Match)):
    prev_matches = [
        match for match in nomination_event_db.bracket.matches if match.next_bracket_match_id == match_db.id
    ]

    if len(prev_matches) == 0:
        return True
    if prev_matches[0].last_result_creator is None:
        return False
    if prev_matches[1].last_result_creator is None:
        return False
    return True
