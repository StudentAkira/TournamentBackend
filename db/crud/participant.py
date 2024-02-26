from typing import cast

from pydantic import EmailStr
from sqlalchemy.orm import Session

from db import models
from db.schemas.participant import ParticipantSchema


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
