from typing import cast

from pydantic import EmailStr
from sqlalchemy.orm import Session

from db import models
from db.crud.nomination_event import get_nomination_event_db
from db.schemas.team import TeamSchema, TeamToEventNominationSchema
from sqlalchemy import and_


def create_team_db(db: Session, team: TeamSchema, participants_emails: set[EmailStr], creator_id: int):
    team_db = models.Team(name=team.name)
    team_db.creator_id = creator_id
    participants_db = db.query(models.Participant).filter(models.Participant.email.in_(participants_emails)).all()
    team_db.participants.extend(participants_db)
    db.add(team_db)
    db.commit()
    return team_db


def get_teams_by_event_nomination_db(
        db: Session,
        nomination_name: str,
        event_name: str,
) -> list[type(models.Team)] | None:
    nomination_event_db = get_nomination_event_db(db, nomination_name, event_name)
    if nomination_event_db:
        teams_db = nomination_event_db.teams
        return teams_db


def get_team_by_name_db(db: Session, team_name: str) -> type(models.Team) | None:
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


def get_teams_db(db: Session, offset: int, limit: int) -> list[type(models.Team)]:
    teams_db = db.query(models.Team).offset(offset).limit(limit).all()
    return teams_db


def append_team_to_nomination_event_db(
        db: Session,
        team_nomination_event_data: TeamToEventNominationSchema
):
    team_name = team_nomination_event_data.team_name
    participant_emails = team_nomination_event_data.participant_emails
    nomination_name = team_nomination_event_data.nomination_name
    event_name = team_nomination_event_data.event_name

    team_id = db.query(models.Team.id).filter(
        cast("ColumnElement[bool]", models.Team.name == team_name)
    ).first()[0]

    participant_ids = db.query(models.Participant.id).filter(models.Participant.email.in_(set(participant_emails))).all()

    set_participant_ids = set()
    for participant_id in participant_ids:
        set_participant_ids.add(participant_id[0])

    nomination_event_db = get_nomination_event_db(db, nomination_name, event_name)

    team_participants = db.query(models.TeamParticipant).filter(
        and_(
            models.TeamParticipant.team_id == team_id,
            models.TeamParticipant.participant_id.in_(set_participant_ids)
        )
    ).all()

    nomination_event_db.team_participants.extend(team_participants)
    db.add(nomination_event_db)
    set_software_equipment_db(
        db,
        nomination_event_db,
        team_nomination_event_data.software,
        team_nomination_event_data.equipment
    )
    db.commit()


def set_software_equipment_db(db, nomination_event_db: type(models.NominationEvent), software: str, equipment: str):

    team_participant_nomination_events_db = db.query(models.TeamParticipantNominationEvent).filter(
        and_(
            models.TeamParticipantNominationEvent.nomination_event_id == nomination_event_db.id,
            models.TeamParticipantNominationEvent.team_participant_id.in_(
                set(team_participant.id for team_participant in nomination_event_db.team_participants)
            )
        )
    )

    for team_participant_nomination_event_db in team_participant_nomination_events_db:
        team_participant_nomination_event_db.software = software
        team_participant_nomination_event_db.equipment = equipment
        db.add(team_participant_nomination_event_db)

