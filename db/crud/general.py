from sqlalchemy import and_
from sqlalchemy.orm import Session

from db import models
from db.schemas.nomination import NominationSchema
from db.schemas.nomination_event import NominationEventSchema
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


def get_nomination_events_info_db(db: Session, events_db: list[models.Event]):
    nomination_event_full_info_list = []
    for event_db in events_db:
        for nomination_db in event_db.nominations:
            nomination_event_db = db.query(models.NominationEvent). \
                filter(and_(models.NominationEvent.nomination_id == nomination_db.id,
                            models.NominationEvent.event_id == event_db.id)).first()

            team_ids = set(team_participant.team_id for team_participant in nomination_event_db.team_participants)

            team_id_data = db.query(models.Team.id, models.Team).filter(models.Team.id.in_(team_ids)).all()

            team_id_names_dict = {key: value for key, value in team_id_data}

            teams = []

            for team_id in team_ids:
                team = team_id_names_dict[team_id]
                teams.append(team)

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
