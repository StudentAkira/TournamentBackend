from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.crud.general import round_robin
from db.models.event import Event
from db.models.group import Group
from db.models.match import Match
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.team import Team
from db.schemas.group_tournament import StartGroupTournamentSchema, GetGroupsOfTournamentSchema, GroupSchema
from db.schemas.nomination_event import NominationEventSchema
from db.schemas.participant import ParticipantSchema
from db.schemas.team import TeamSchema
from db.schemas.team_participant import TeamParticipantsSchema


def create_group_tournament_db(db: Session, nomination_event: StartGroupTournamentSchema):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == nomination_event.event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_event.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == nomination_event.type
        )
    ).first()

    nomination_event_db.tournament_started = True

    team_ids = set(team_participant_db.team_id for team_participant_db in nomination_event_db.team_participants)
    teams_db = db.query(Team).filter(Team.id.in_(team_ids)).all()
    groups = [Group() for i in range(nomination_event.group_count)]
    index = 0
    while teams_db:
        groups[index % nomination_event.group_count].teams.append(teams_db.pop(0))
        index += 1

    for group in groups:
        matches_data = round_robin(group.teams.copy())
        for i, match_data in enumerate(matches_data):
            winner = None
            if match_data[0] is None and match_data[1] is not None:
                winner = match_data[1]
            if match_data[1] is None and match_data[0] is not None:
                winner = match_data[0]
            match_db = Match(
                match_queue_number=i+1,
                team1=match_data[0],
                team2=match_data[1],
                winner=winner
            )
            group.matches.append(match_db)
            db.add(match_db)
        db.add(group)
    nomination_event_db.groups.extend(groups)
    db.add(nomination_event_db)
    db.commit()


def get_count_of_participants_of_tournament_db(
        db: Session,
        nomination_name: str,
        event_name: str,
        nomination_event_type: str
):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name ==nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == nomination_event_type
        )
    ).first()
    count = len(nomination_event_db.team_participants)
    return count


def get_groups_of_tournament_db(db: Session, nomination_event: NominationEventSchema):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == nomination_event.event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_event.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == nomination_event.type
        )
    ).first()

    result = GetGroupsOfTournamentSchema(
        groups=[
            GroupSchema(
                id=group_db.id,
                teams=[
                    TeamSchema(
                        name=team_db.name,
                    ) for team_db in group_db.teams
                ]
            ) for group_db in nomination_event_db.groups
        ]
    )
    return result


def is_all_matches_finished_db(db: Session, nomination_event: NominationEventSchema):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == nomination_event.event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_event.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == nomination_event.type
        )
    ).first()

    for group in nomination_event_db.groups:
        for match in group.matches:
            if match.last_result_creator is None and match.team1 is not None and match.team2 is not None:
                return False
    return True


def finish_group_stage_db(db: Session, nomination_event: NominationEventSchema):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == nomination_event.event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_event.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == nomination_event.type
        )
    ).first()

    nomination_event_db.group_stage_finished = True
    db.add(nomination_event_db)
    db.commit()


def start_play_off_tournament_db(db: Session, nomination_event: NominationEventSchema):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == nomination_event.event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_event.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == nomination_event.type
        )
    ).first()

    for group in nomination_event_db.groups:
        team_score = {}
        for match in group.matches:

            if match.team1:
                team_score[match.team1.id] = team_score.get(match.team1.id, 0)\
                                             + (1 if match.winner.id == match.team1.id else 0)
            if match.team2:
                team_score[match.team2.id] = team_score.get(match.team2.id, 0)\
                                             + (1 if match.winner.id == match.team2.id else 0)
        print(group.id)
        print(team_score)
