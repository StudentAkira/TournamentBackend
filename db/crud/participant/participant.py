from typing import cast

from pydantic import EmailStr
from sqlalchemy.orm import Session

from db.models.participant import Participant
from db.models.team import Team
from db.schemas.participant.participant import ParticipantSchema
from db.schemas.participant.participant_update import ParticipantUpdateSchema


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
    participants_db = db.query(Participant).\
        filter(cast("ColumnElement[bool]", Participant.creator_id == owner_id)).\
        filter(cast("ColumnElement[bool]", Participant.hidden == "f")).\
        offset(offset).limit(limit)

    participants = [ParticipantSchema.from_orm(participant_db) for participant_db in participants_db]
    return participants


def hide_participant_db(db: Session, participant_db: type(Participant)):
    participant_db.hidden = True
    db.add(participant_db)
    db.commit()


def update_participant_db(db: Session, participant_db: type(Participant), participant_data: ParticipantUpdateSchema):
    team_db = db.query(Team).filter(
        cast("ColumnElement[bool]", Team.name == f"default_team_{participant_data.old_email}")
    ).first()
    participant_db.email = participant_data.new_email
    team_db.name = f"default_team_{participant_data.new_email}"
    db.add(participant_db)
    db.add(team_db)
    db.commit()
