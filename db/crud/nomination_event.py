from typing import cast

from sqlalchemy.orm import Session

from db import models
from db.crud.event import get_all_events_db, get_all_events_by_owner_db
from db.crud.nominations import get_all_nominations_db
from db.schemas.nomination_event import NominationEventSchema, NominationEventNameSchema
from db.schemas.participant import ParticipantSchema
from db.schemas.team import TeamSchema, TeamParticipantsSchema


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
    nomination_event_db = db.query(models.NominationEvent) \
        .filter(models.NominationEvent.event_id == event_db.id
                and models.NominationEvent.nomination_id == nomination_db.id).first()
    return nomination_event_db


def get_nomination_events_full_info_db(db: Session, offset: int, limit: int):
    events_db = get_all_events_db(db)
    nominations_db = get_all_nominations_db(db)

    event_id_name_pairs = {event_db.id: event_db.name for event_db in events_db}
    nomination_id_name_pairs = {nomination_db.id: nomination_db.name for nomination_db in nominations_db}

    nominations_events_db = db.query(models.NominationEvent). \
        filter(models.NominationEvent.event_id.in_(event_id_name_pairs)). \
        offset(offset).limit(limit).all()

    nomination_events = []

    for nomination_event_db in nominations_events_db:
        nomination_events.append(
            NominationEventSchema(
                event_name=event_id_name_pairs[nomination_event_db.event_id],
                nomination_name=nomination_id_name_pairs[nomination_event_db.nomination_id],
                teams=[TeamParticipantsSchema(
                    name=team_db.name,
                    participants=[
                        ParticipantSchema.from_orm(participant_db)
                        for participant_db in team_db.participants
                    ]
                ) for team_db in nomination_event_db.teams
                ]
            )
        )

    return nomination_events


def get_nomination_events_full_info_by_owner_db(
        db: Session,
        offset: int,
        limit: int,
        owner_id: int
) -> list[type(models.NominationEvent)]:
    events_db = get_all_events_by_owner_db(db, owner_id)
    nominations_db = get_all_nominations_db(db)

    event_id_name_pairs = {event_db.id: event_db.name for event_db in events_db}
    nomination_id_name_pairs = {nomination_db.id: nomination_db.name for nomination_db in nominations_db}

    nominations_events_db = db.query(models.NominationEvent). \
        filter(models.NominationEvent.event_id.in_(event_id_name_pairs)). \
        offset(offset).limit(limit).all()

    nomination_events = []

    for nomination_event_db in nominations_events_db:
        nomination_events.append(
            NominationEventSchema(
                event_name=event_id_name_pairs[nomination_event_db.event_id],
                nomination_name=nomination_id_name_pairs[nomination_event_db.nomination_id],
                teams=[TeamParticipantsSchema(
                    name=team_db.name,
                    participants=[
                        ParticipantSchema.from_orm(participant_db)
                        for participant_db in team_db.participants
                    ]
                ) for team_db in nomination_event_db.teams
                ]
            )
        )

    return nomination_events


def get_nomination_events_names_db(db: Session, offset: int, limit: int):
    events_db = get_all_events_db(db)
    nominations_db = get_all_nominations_db(db)

    event_id_name_pairs = {event_db.id: event_db.name for event_db in events_db}
    nomination_id_name_pairs = {nomination_db.id: nomination_db.name for nomination_db in nominations_db}

    nominations_events_db = db.query(models.NominationEvent). \
        filter(models.NominationEvent.event_id.in_(event_id_name_pairs)). \
        offset(offset).limit(limit).all()

    nomination_events = []

    for nomination_event_db in nominations_events_db:
        nomination_events.append(
            NominationEventNameSchema(
                event_name=event_id_name_pairs[nomination_event_db.event_id],
                nomination_name=nomination_id_name_pairs[nomination_event_db.nomination_id],
            )
        )

    return nomination_events


def get_nomination_events_names_by_owner_db(db: Session, offset: int, limit: int, owner_id: int):
    events_db =  get_all_events_by_owner_db(db, owner_id)
    nominations_db = get_all_nominations_db(db)

    event_id_name_pairs = {event_db.id: event_db.name for event_db in events_db}
    nomination_id_name_pairs = {nomination_db.id: nomination_db.name for nomination_db in nominations_db}

    nominations_events_db = db.query(models.NominationEvent). \
        filter(models.NominationEvent.event_id.in_(event_id_name_pairs)). \
        offset(offset).limit(limit).all()

    nomination_events = []

    for nomination_event_db in nominations_events_db:
        nomination_events.append(
            NominationEventNameSchema(
                event_name=event_id_name_pairs[nomination_event_db.event_id],
                nomination_name=nomination_id_name_pairs[nomination_event_db.nomination_id],
            )
        )

    return nomination_events