from typing import cast

from pydantic import EmailStr
from sqlalchemy.orm import Session

from db.crud.nomination_event import get_nomination_event_db
from db.models.nomination_event import NominationEvent
from db.models.participant import Participant
from db.models.team import Team
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.schemas.team import TeamSchema, TeamUpdateSchema

from sqlalchemy import and_


def create_team_db(db: Session, team: TeamSchema, participants_emails: set[EmailStr], creator_id: int):
    team_db = Team(name=team.name)
    team_db.creator_id = creator_id
    participants_db = db.query(Participant).filter(Participant.email.in_(participants_emails)).all()
    team_db.participants.extend(participants_db)
    db.add(team_db)
    db.commit()
    return team_db


def get_teams_by_event_nomination_db(
        db: Session,
        nomination_name: str,
        event_name: str,
) -> list[type(Team)] | None:
    nomination_event_db = get_nomination_event_db(db, nomination_name, event_name)
    if nomination_event_db:
        teams_db = nomination_event_db.teams
        return teams_db


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
    teams_db = db.query(Team).filter(
        cast("ColumnElement[bool]", Team.creator_id == owner_id)
    ).offset(offset).limit(limit).all()
    return teams_db


def get_teams_db(db: Session, offset: int, limit: int) -> list[type(Team)]:
    teams_db = db.query(Team).offset(offset).limit(limit).all()
    return teams_db


def update_team_db(db:Session, team_data: TeamUpdateSchema):
    team_db = db.query(Team).filter(
        cast("ColumnElement[bool]", Team.name == team_data.old_name
             )).first()
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
