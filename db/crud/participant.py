from typing import cast

from pydantic import EmailStr
from sqlalchemy.orm import Session

from db import models
from db.crud.team import get_team_by_name_db
from db.schemas.participant import ParticipantSchema
from db.schemas.team import TeamSchema


def create_participant_db(db: Session, participant: ParticipantSchema, creator_id: int) -> type(models.Participant):
    participant_db = models.Participant(**participant.model_dump())
    participant_db.creator_id = creator_id
    team_db = models.Team(name=f"default_team_{participant.email}", creator_id=participant_db.creator_id)
    db.add(participant_db)
    db.add(team_db)
    db.commit()
    return participant_db


def get_participant_by_email_db(db: Session, email: EmailStr) -> type(models.Participant) | None:
    participant = db.query(models.Participant).filter(
        cast("ColumnElement[bool]", models.Participant.email == email)
    ).first()
    return participant


def get_participants_by_owner_db(
        db: Session,
        offset: int,
        limit: int,
        owner_id: int
) -> list[type(models.Participant)] | None:
    participants_db = db.query(models.Participant).filter(
        cast("ColumnElement[bool]", models.Participant.creator_id == owner_id)
    ).offset(offset).limit(limit)

    participants = [ParticipantSchema.from_orm(participant_db) for participant_db in participants_db]
    return participants


def get_emails_of_teams_members(teams: list[type(models.Team)]) -> list[str]:
    participants_emails = []
    for team_db in teams:
        for participant in team_db.participants:
            participants_emails.append(participant.email)
    return participants_emails


def append_participant_to_team_db(db: Session, participant: ParticipantSchema, team: TeamSchema):

    participant_db = db.query(models.Participant).filter(
        cast("ColumnElement[bool]", models.Participant.email == participant.email)
    ).first()

    team_db = db.query(models.Team).filter(
        cast("ColumnElement[bool]", models.Team.name == team.name)
    ).first()

    participant_db.teams.append(team_db)
    db.add(participant_db)
    db.commit()


def check_if_participant_already_in_team_db(db: Session, participant: ParticipantSchema, team: TeamSchema) -> bool:
    participant_db = get_participant_by_email_db(db, participant.email)
    team_db = get_team_by_name_db(db, team.name)
    return team_db in set(participant_db.teams)
