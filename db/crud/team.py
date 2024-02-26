from typing import cast

from pydantic import EmailStr
from sqlalchemy.orm import Session

from db import models
from db.crud.nomination_event import get_nomination_event_db
from db.schemas.team import TeamSchema


def create_team_db(db: Session, team: TeamSchema, creator_id: int):
    team_db = models.Team(name=team.name)
    team_db.creator_id = creator_id
    db.add(team_db)
    db.commit()
    return team_db


def get_teams_by_event_nomination_db(
        db: Session,
        event_name: str,
        nomination_name: str
) -> list[type(models.Team)] | None:
    nomination_event_db = get_nomination_event_db(db, event_name, nomination_name)
    if nomination_event_db:
        teams_db = nomination_event_db.teams
        return teams_db


def get_team_by_name_db(db: Session, team_name: str) -> type(models.Team):
    team_db = db.query(models.Team).filter(
        cast("ColumnElement[bool]", models.Team.name == team_name)
             ).first()
    return team_db


def get_team_participants_emails_db(db: Session, team_name: str) -> list[EmailStr]:
    team_db = get_team_by_name_db(db, team_name)
    participants_emails = [participant.email for participant in team_db.participants]
    return participants_emails


def get_teams_by_owner_db(db: Session, offset: int, limit: int, owner_id: int) -> list[type(models.Team)]:
    teams_db = db.query(models.Team).filter(
        cast("ColumnElement[bool]", models.Team.creator_id == owner_id)
    ).offset(offset).limit(limit).all()
    return teams_db
