from sqlalchemy import and_
from sqlalchemy.orm import Session

from db import models
from db.models import Nomination, Event
from db.schemas.event import EventListSchema
from db.schemas.nomination import NominationSchema
from db.schemas.nomination_event import NominationEventSchema, NominationEventNameSchema
from db.schemas.team import TeamParticipantsSchema


def create_missing_items(
        db: Session,
        model_name: type(models.Nomination),
        items: list[NominationSchema]
) -> list[type(models.Nomination)]:
    all_items = db.query(model_name).all()
    existing_items_names = {db_item.name for db_item in all_items}

    new_items = [
        model_name(name=item.name)
        for item in items
        if item.name not in existing_items_names
    ]
    received_items_names = {item.name for item in items}
    created_items_names = {item.name for item in new_items}

    existing_items = [
        item for item in db.query(model_name).filter(
            model_name.name.in_(received_items_names - created_items_names)
        ).all()
    ]

    for db_item in new_items:
        db.add(db_item)

    return existing_items + new_items


def get_nomination_events_info_db(db: Session, events_db: list[type(models.Event)]):
    nomination_event_full_info_list = []
    for event_db in events_db:
        for nomination_db in event_db.nominations:
            nomination_event_db = db.query(models.NominationEvent). \
                filter(and_(models.NominationEvent.nomination_id == nomination_db.id,
                            models.NominationEvent.event_id == event_db.id)).first()

            team_ids = set(team_participant.team_id for team_participant in nomination_event_db.team_participants)
            teams = db.query(models.Team).filter(models.Team.id.in_(team_ids)).all()
            nomination_event_full_info = NominationEventSchema(
                event_name=event_db.name,
                nomination_name=nomination_db.name,
                teams=[
                    TeamParticipantsSchema.from_orm(
                        team
                    ) for team in teams
                ]
            )

            nomination_event_full_info_list.append(nomination_event_full_info)
    return nomination_event_full_info_list


def get_nomination_events_names_db(
        db: Session,
        nominations_db: list[type(Nomination)],
        events_db: list[type(Event)],
        offset: int,
        limit: int
):

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


def get_events_data(events_db: list[type(models.Event)]):
    events_data = []
    for event_db in events_db:
        events_data.append(EventListSchema.from_orm(event_db))
    return events_data
