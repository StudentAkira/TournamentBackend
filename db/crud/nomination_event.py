from typing import cast

from sqlalchemy.orm import Session

from db import models
from db.crud.event import get_all_events_db, get_all_events_by_owner_db
from db.crud.general import get_nomination_events_info_db, get_nomination_events_names_db
from db.crud.nominations import get_all_nominations_db
from db.schemas.nomination_event import NominationEventNameSchema, NominationEventSchema
from sqlalchemy import and_


def get_nomination_and_event_ids(db: Session, offset: int, limit: int):
    nominations_events_db = db.query(models.NominationEvent).offset(offset).limit(limit).all()

    nomination_ids = []
    event_ids = []

    for nomination_event_db in nominations_events_db:
        nomination_ids.append(nomination_event_db.nomination_id)
        event_ids.append(nomination_event_db.event_id)
    return nomination_ids, event_ids


def get_nomination_event_db(
        db: Session,
        nomination_name: str,
        event_name: str,
) -> type(models.NominationEvent) | None:
    event_db = db.query(models.Event).filter(
        cast("ColumnElement[bool]", models.Event.name == event_name)
    ).first()
    nomination_db = db.query(models.Nomination).filter(
        cast("ColumnElement[bool]", models.Nomination.name == nomination_name)
    ).first()

    nomination_event_db = db.query(models.NominationEvent).\
        filter(and_(models.NominationEvent.event_id == event_db.id,
                    models.NominationEvent.nomination_id == nomination_db.id)).first()
    return nomination_event_db


def get_nomination_events_full_info_db(
        db: Session,
        offset: int,
        limit: int
) -> list[NominationEventSchema]:
    events_db = db.query(models.Event).offset(offset).limit(limit).all()
    return get_nomination_events_info_db(db, events_db)


def get_nomination_events_full_info_by_owner_db(
        db: Session,
        offset: int,
        limit: int,
        owner_id: int
) -> list[NominationEventSchema]:
    events_db = db.query(models.Event).\
        filter(cast("ColumnElement[bool]", models.Event.owner_id == owner_id)).\
        offset(offset).limit(limit).all()
    return get_nomination_events_info_db(db, events_db)


def get_nomination_event_teams_db(db: Session, nomination_name: str, event_name: str):

    event_id = db.query(models.Event.id).filter(
        cast("ColumnElement[bool]", models.Event.name == event_name)
    ).first()[0]
    nomination_id = db.query(models.Nomination.id).filter(
        cast("ColumnElement[bool]", models.Nomination.name == nomination_name)
    ).first()[0]

    nomination_event_id = db.query(models.NominationEvent.id).filter(
        and_(
            models.NominationEvent.nomination_id == nomination_id, models.NominationEvent.event_id == event_id
        )
    ).first()[0]

    team_participant_ids = db.query(models.TeamParticipantNominationEvent.team_participant_id).\
        filter(models.TeamParticipantNominationEvent.nomination_event_id == nomination_event_id).all()

    set_team_participant_ids = set()
    for team_participant_id in team_participant_ids:
        set_team_participant_ids.add(team_participant_id[0])

    team_ids = set(db.query(models.TeamParticipant.team_id).
                   filter(models.TeamParticipant.id.in_(set_team_participant_ids)).all())

    set_team_ids = set()
    for team_id in team_ids:
        set_team_ids.add(team_id[0])

    teams_db = db.query(models.Team).filter(models.Team.id.in_(set_team_ids))

    return teams_db


def get_nomination_events_all_names_db(db: Session, offset: int, limit: int):
    events_db = get_all_events_db(db)
    nominations_db = get_all_nominations_db(db)
    return get_nomination_events_names_db(db, nominations_db, events_db, offset, limit)


def get_nomination_events_all_names_by_owner_db(db: Session, offset: int, limit: int, owner_id: int):
    events_db = get_all_events_by_owner_db(db, owner_id)
    nominations_db = get_all_nominations_db(db)
    return get_nomination_events_names_db(db, nominations_db, events_db, offset, limit)