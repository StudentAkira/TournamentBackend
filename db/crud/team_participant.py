from typing import cast

from pydantic import EmailStr
from sqlalchemy.orm import Session

from db.crud.participant import get_participant_by_email_db
from db.crud.team import get_team_by_name_db
from db.models.participant import Participant
from db.models.team import Team
from db.schemas.participant import ParticipantSchema
from db.schemas.team import TeamSchema


def get_emails_of_teams_participants_db(teams: list[type(Team)]) -> list[str]:
    participants_emails = []
    for team_db in teams:
        for participant in team_db.participants:
            participants_emails.append(participant.email)
    return participants_emails


def append_participant_to_team_db(db: Session, participant: ParticipantSchema, team: TeamSchema):

    participant_db = db.query(Participant).filter(
        cast("ColumnElement[bool]", Participant.email == participant.email)
    ).first()

    team_db = db.query(Team).filter(
        cast("ColumnElement[bool]", Team.name == team.name)
    ).first()

    participant_db.teams.append(team_db)
    db.add(participant_db)
    db.commit()


def check_if_participant_already_in_team_db(db: Session, participant: ParticipantSchema, team: TeamSchema) -> bool:
    participant_db = get_participant_by_email_db(db, participant.email)
    team_db = get_team_by_name_db(db, team.name)
    return team_db in set(participant_db.teams)


def delete_participant_from_team_db(db: Session, participant_email: EmailStr, team_name: str):

    participant_db = db.query(Participant).filter(
        cast("ColumnElement[bool]", Participant.email == participant_email)
    ).first()

    team_db = db.query(Team).filter(
        cast("ColumnElement[bool]", Team.name == team_name)
    ).first()

    participant_db.teams.remove(team_db)
    db.add(participant_db)
    db.commit()
