from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.crud.general import round_robin
from db.models.bracket import Bracket
from db.models.event import Event
from db.models.group import Group
from db.models.match import Match
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.team import Team
from db.schemas.group_tournament import StartGroupTournamentSchema, GetGroupsOfTournamentSchema, GroupSchema
from db.schemas.nomination_event import OlympycNominationEventSchema, NominationEventType
from db.schemas.team import TeamSchema


def create_group_tournament_db(db: Session, nomination_event: StartGroupTournamentSchema):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == nomination_event.olympyc_nomination_event.event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_event.olympyc_nomination_event.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == NominationEventType.olympyc
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
        nomination_event: OlympycNominationEventSchema
):
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
    count = len(nomination_event_db.team_participants)
    return count


def get_groups_of_tournament_db(db: Session, nomination_event: OlympycNominationEventSchema):
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


def is_all_matches_finished_db(db: Session, nomination_event: OlympycNominationEventSchema):
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

    for group in nomination_event_db.groups:
        for match in group.matches:
            if match.last_result_creator is None and match.team1 is not None and match.team2 is not None:
                return False
    if nomination_event_db.bracket:
        for match in nomination_event_db.bracket.matches:
            if match.last_result_creator is None:
                return False
    return True


def finish_group_stage_db(db: Session, nomination_event: OlympycNominationEventSchema):
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

    nomination_event_db.group_stage_finished = True
    db.add(nomination_event_db)
    db.commit()


def finish_play_off_stage_db(db: Session, nomination_event: OlympycNominationEventSchema):
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

    nomination_event_db.play_off_stage_finished = True
    db.add(nomination_event_db)
    db.commit()



def start_play_off_tournament_db(db: Session, nomination_event: OlympycNominationEventSchema, teams: list[TeamSchema]):
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

    team_score = {}

    for group in nomination_event_db.groups:

        for match in group.matches:

            if match.team1:
                team_score[match.team1.id] = team_score.get(match.team1.id, 0)\
                                             + (1 if
                                                match.winner is not None and match.winner.id == match.team1.id
                                                else 0)
            if match.team2:
                team_score[match.team2.id] = team_score.get(match.team2.id, 0)\
                                             + (1 if
                                                match.winner is not None and match.winner.id == match.team2.id
                                                else 0)

    receive_team_names = set(team_db.name for team_db in teams)
    received_team_ids = set(team_db.id for team_db in db.query(Team).filter(Team.name.in_(receive_team_names)))

    teams_to_create_matches = sorted(
        [
            (k, team_score[k])
            for k in team_score.keys() if k in received_team_ids],
        key=lambda item: item[1],
        reverse=True
    )

    team_count = 2
    while team_count < len(teams):
        team_count *= 2
    while team_count > len(teams_to_create_matches):
        teams_to_create_matches.append((None, 0))

    # print(teams_to_create_matches)

    teams_ids = [team[0] for team in teams_to_create_matches]
    teams_db = db.query(Team).filter(Team.id.in_(teams_ids)).all()

    team_id_entity = {team_db.id: team_db for team_db in teams_db}

    matches = []
    last = len(teams_to_create_matches) - 1
    first = 0

    bracket_db = Bracket()
    nomination_event_db.bracket = bracket_db
    bracket_db.nomination_event = nomination_event_db
    db.add(bracket_db)
    db.add(nomination_event_db)
    db.commit()

    while last > first:

        team1_id = teams_to_create_matches[first][0]
        team2_id = teams_to_create_matches[last][0]

        match_db = Match(
            team1_id=team1_id if team1_id is not None else None,
            team2_id=team2_id if team2_id is not None else None
        )
        match_db.bracket = bracket_db
        match_db.team1 = team_id_entity[team1_id] if team1_id is not None else None
        match_db.team2 = team_id_entity[team2_id] if team2_id is not None else None
        matches.append(match_db)

        db.add(match_db)

        last -= 1
        first += 1

    print([
        (
            match_db.team1.id if match_db.team1 is not None else None,
            match_db.team2.id if match_db.team2 is not None else None
        )
        for match_db in matches
    ])
    while len(matches) > 1:
        tmp_matches = []
        for i in range(0, len(matches), 2):
            match_db = Match()
            matches[i].next_bracket_match = match_db
            matches[i + 1].next_bracket_match = match_db

            match_db.bracket = bracket_db
            db.add(match_db)

            tmp_matches.append(match_db)
        matches = tmp_matches.copy()

        print([
            (match_db.team1_id, match_db.team2_id) for match_db in tmp_matches
        ])

    db.add(bracket_db)
    db.add(nomination_event_db)

    db.commit()


