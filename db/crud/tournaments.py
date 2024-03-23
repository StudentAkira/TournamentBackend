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
            match_db = Match(
                match_queue_number=i+1,
                team1=match_data[0],
                team2=match_data[1],
                winner=None
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
                    TeamParticipantsSchema(
                        name=team_db.name,
                        participants=[
                            ParticipantSchema.from_orm(participant_db)
                            for participant_db in team_db.participants
                        ]
                    ) for team_db in group_db.teams
                ]
            ) for group_db in nomination_event_db.groups
        ]
    )
    return result
