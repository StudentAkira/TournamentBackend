from typing import cast

from sqlalchemy.orm import Session

from db import models
from db.crud.event import get_all_events_db, get_all_events_by_owner_db
from db.crud.nominations import get_all_nominations_db
from db.models import TeamParticipantNominationEvent
from db.schemas.nomination_event import NominationEventSchema, NominationEventNameSchema
from db.schemas.participant import ParticipantSchema
from db.schemas.team import TeamParticipantsSchema
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


def get_nomination_events_full_info_db(db: Session, offset: int, limit: int):
    events_db = db.query(models.Event).all()
    for event_db in events_db:
        for nomination_db in event_db.nominations:
            teams_db = get_nomination_event_teams_db(db, nomination_db.name, event_db.name)
            team_names = [team_db.name for team_db in teams_db]
            print(event_db.name, nomination_db.name, team_names)


def get_nomination_events_full_info_by_owner_db(db: Session, offset: int, limit: int, owner_id: int):
    nomination_events = db.query(models.NominationEvent).offset(offset).limit(limit).all()


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

# def get_nomination_events_full_info_db(db: Session, offset: int, limit: int):
#     events_db = get_all_events_db(db)
#     nominations_db = get_all_nominations_db(db)
#
#     event_id_name_pairs = {event_db.id: event_db.name for event_db in events_db}
#     nomination_id_name_pairs = {nomination_db.id: nomination_db.name for nomination_db in nominations_db}
#
#     nominations_events_db = db.query(models.NominationEvent). \
#         filter(models.NominationEvent.event_id.in_(event_id_name_pairs)). \
#         offset(offset).limit(limit).all()
#
#     nomination_events = []
#
#     for nomination_event_db in nominations_events_db:
#         nomination_events.append(
#             NominationEventSchema(
#                 event_name=event_id_name_pairs[nomination_event_db.event_id],
#                 nomination_name=nomination_id_name_pairs[nomination_event_db.nomination_id],
#                 teams=[TeamParticipantsSchema(
#                     name=team_db.name,
#                     participants=[
#                         ParticipantSchema.from_orm(participant_db)
#                         for participant_db in team_db.participants
#                     ]
#                 ) for team_db in nomination_event_db.teams
#                 ]
#             )
#         )
#
#     return nomination_events
#
#
# def get_nomination_events_full_info_by_owner_db(
#         db: Session,
#         offset: int,
#         limit: int,
#         owner_id: int
# ) -> list[type(models.NominationEvent)]:
#     events_db = get_all_events_by_owner_db(db, owner_id)
#     nominations_db = get_all_nominations_db(db)
#
#     event_id_name_pairs = {event_db.id: event_db.name for event_db in events_db}
#     nomination_id_name_pairs = {nomination_db.id: nomination_db.name for nomination_db in nominations_db}
#
#     nominations_events_db = db.query(models.NominationEvent). \
#         filter(models.NominationEvent.event_id.in_(event_id_name_pairs)). \
#         offset(offset).limit(limit).all()
#
#     nomination_events = []
#
#     for nomination_event_db in nominations_events_db:
#         nomination_events.append(
#             NominationEventSchema(
#                 event_name=event_id_name_pairs[nomination_event_db.event_id],
#                 nomination_name=nomination_id_name_pairs[nomination_event_db.nomination_id],
#                 teams=[TeamParticipantsSchema(
#                     name=team_db.name,
#                     participants=[
#                         ParticipantSchema.from_orm(participant_db)
#                         for participant_db in team_db.participants
#                     ]
#                 ) for team_db in nomination_event_db.teams
#                 ]
#             )
#         )
#
#     return nomination_events


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