from typing import cast

from pydantic import EmailStr
from sqlalchemy.orm import Session

from db.models.participant import Participant
from db.models.team import Team
from db.schemas.participant import ParticipantSchema


def create_participant_db(db: Session, participant: ParticipantSchema, creator_id: int) -> type(Participant):
    participant_db = Participant(**participant.model_dump())
    participant_db.creator_id = creator_id
    team_db = Team(name=f"default_team_{participant.email}", creator_id=participant_db.creator_id)
    participant_db.teams.append(team_db)
    db.add(participant_db)
    db.add(team_db)
    db.commit()
    return participant_db


def get_participant_by_email_db(db: Session, email: EmailStr) -> type(Participant) | None:
    participant = db.query(Participant).filter(
        cast("ColumnElement[bool]", Participant.email == email)
    ).first()
    return participant


def get_participants_by_owner_db(
        db: Session,
        offset: int,
        limit: int,
        owner_id: int
) -> list[type(Participant)] | None:
    participants_db = db.query(Participant).filter(
        cast("ColumnElement[bool]", Participant.creator_id == owner_id)
    ).offset(offset).limit(limit)

    participants = [ParticipantSchema.from_orm(participant_db) for participant_db in participants_db]
    return participants




# def get_participants_of_team_db(db: Session, team_name: str):
#     # team_db = db.query(Team).filter( cast("ColumnElement[bool]", Team.name == team_name)).first()
#     pass
