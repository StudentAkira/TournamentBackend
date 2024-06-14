from typing import cast

from pydantic import EmailStr
from sqlalchemy import and_, not_
from sqlalchemy.orm import Session

from db.crud.nomination_event.nomination_event import get_nomination_event_db
from db.models.nomination_event import NominationEvent
from db.models.team import Team
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.schemas.team.team import TeamSchema
from db.schemas.team.team_update import TeamUpdateSchema


def create_team_db(db: Session, team: TeamSchema, creator_id: int):
    team_db = Team(name=team.name)
    team_db.creator_id = creator_id
    db.add(team_db)
    db.commit()
    return team_db


def get_team_by_name_db(db: Session, team_name: str) -> type(Team) | None:
    team_db = db.query(Team).filter(
        cast("ColumnElement[bool]", Team.name == team_name)
    ).first()
    return team_db


def get_team_participants_emails_db(db: Session, team_name: str) -> list[EmailStr]:
    team_db = get_team_by_name_db(db, team_name)
    participants_emails = [participant.email for participant in team_db.participants]
    return participants_emails


def get_teams_by_owner_db(db: Session, offset: int, limit: int, owner_id: int) -> list[type(Team)]:
    teams_db = db.query(Team).filter(and_(
        cast("ColumnElement[bool]", Team.creator_id == owner_id),
        cast("ColumnElement[bool]", not_(Team.name.ilike("%default_team%")))
    )
    ).offset(offset).limit(limit).all()
    return teams_db


def get_teams_db(db: Session, offset: int, limit: int) -> list[type(Team)]:
    teams_db = db.query(Team).filter(
        cast("ColumnElement[bool]",
             not_(Team.name.ilike("%default_team%")))
    ).offset(offset).limit(limit).all()
    return teams_db


def update_team_db(db: Session, team_db: type(Team), team_data: TeamUpdateSchema):
    team_db.name = team_data.new_name
    db.add(team_db)
    db.commit()


def set_software_equipment_db(db, nomination_event_db: type(NominationEvent), software: str, equipment: str):
    team_participant_nomination_events_db = db.query(TeamParticipantNominationEvent).filter(
        and_(
            TeamParticipantNominationEvent.nomination_event_id == nomination_event_db.id,
            TeamParticipantNominationEvent.team_participant_id.in_(
                set(team_participant.id for team_participant in nomination_event_db.team_participants)
            )
        )
    )

    for team_participant_nomination_event_db in team_participant_nomination_events_db:
        team_participant_nomination_event_db.software = software
        team_participant_nomination_event_db.equipment = equipment
        db.add(team_participant_nomination_event_db)


def team_check_existence_in_tournament_db(
        db: Session,
        teams: list[TeamSchema],
        nomination_event_db: type(NominationEvent)
):
    team_names = [team.name for team in teams]
    received_teams_ids = set(team_db.id for team_db in db.query(Team).filter(Team.name.in_(team_names)).all())
    tournament_team_ids = set(team_participant.team_id for team_participant in nomination_event_db.team_participants)
    if received_teams_ids.issubset(tournament_team_ids):
        return True
    return False
