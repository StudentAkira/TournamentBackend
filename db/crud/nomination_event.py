from typing import cast

from sqlalchemy.orm import Session

from db.crud.event import get_all_events_db, get_all_events_by_owner_db, get_events_data, get_event_by_name_db
from db.crud.nominations import get_all_nominations_db, create_nominations_missing_in_db, get_nomination_by_name_db
from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.team import Team
from db.models.team_participant import TeamParticipant
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.schemas.event import EventListSchema, EventSchema, EventGetNameSchema
from db.schemas.nomination import NominationSchema
from db.schemas.nomination_event import NominationEventSchema, NominationEventDeleteSchema, \
    NominationEventFullInfoSchema, NominationEventParticipantCountSchema
from sqlalchemy import and_

from db.schemas.team_participant import TeamParticipantsSchema


def get_nominations_event_participant_count_db(
        db: Session,
        event_name: str
) -> list[NominationEventParticipantCountSchema]:
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == event_name)
    ).first()
    nomination_events_db = db.query(NominationEvent).\
        filter(
        cast("ColumnElement[bool]", NominationEvent.event_id == event_db.id)
    ).all()

    result = []

    for nomination_event_db in nomination_events_db:

        nomination_db = db.query(Nomination).filter(
            Nomination.id == nomination_event_db.nomination_id
        ).first()

        result.append(
            NominationEventParticipantCountSchema(
                nomination_name=nomination_db.name,
                type=nomination_event_db.type,
                participant_count=len(nomination_event_db.team_participants)
            )
        )

    return result


def append_nomination_for_event_db(
        db: Session,
        nomination_event_data: NominationEventSchema
):
    nomination_db = get_nomination_by_name_db(db, nomination_event_data.nomination_name)
    event_db = get_event_by_name_db(db, nomination_event_data.event_name)
    nomination_event_db = NominationEvent(
        event_id=event_db.id,
        nomination_id=nomination_db.id,
        registration_finished=False,
        type=nomination_event_data.type
    )
    db.add(nomination_event_db)
    db.commit()
    db.refresh(event_db)


def append_event_nominations_db(
        db: Session,
        event: EventGetNameSchema,
        nominations: list[NominationSchema]
) -> type(Event):
    nominations_db = create_nominations_missing_in_db(db, nominations)
    event_db = get_event_by_name_db(db, event.name)
    event_db.nominations.extend(set(nominations_db) - set(event_db.nominations))
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db


def get_list_events_list_nominations_db(db: Session) -> list[EventListSchema]:
    events_db = db.query(Event).all()
    return get_events_data(events_db)


def get_list_events_list_nominations_by_owner_db(db: Session, owner_id: int):
    events_db = db.query(Event).filer(cast("ColumnElement[bool]", Event.owner_id == owner_id)).all()
    return get_events_data(events_db)


def get_nomination_event_db(
        db: Session,
        nomination_name: str,
        event_name: str,
        nomination_event_type: str
) -> type(NominationEvent) | None:
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == event_name)
    ).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_name)
    ).first()

    nomination_event_db = db.query(NominationEvent). \
        filter(and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == nomination_event_type
        )
    ).first()
    return nomination_event_db


def get_nomination_events_info_db(db: Session, events_db: list[type(Event)]):
    nomination_event_full_info_list = []
    for event_db in events_db:
        nominations_event_db = db.query(NominationEvent).filter(
            NominationEvent.event_id == event_db.id
        ).all()
        for nomination_event_db in nominations_event_db:

            team_ids = set(team_participant.team_id for team_participant in nomination_event_db.team_participants)
            teams = db.query(Team).filter(Team.id.in_(team_ids)).all()

            nomination_db = db.query(Nomination).filter(
                Nomination.id == nomination_event_db.nomination_id
            ).first()
            nomination_event_full_info = NominationEventFullInfoSchema(
                event_name=event_db.name,
                nomination_name=nomination_db.name,
                type=nomination_event_db.type,
                teams=[
                    TeamParticipantsSchema.from_orm(
                        team
                    ) for team in teams
                ]
            )

            nomination_event_full_info_list.append(nomination_event_full_info)
    return nomination_event_full_info_list


def get_nomination_events_full_info_db(
        db: Session,
        offset: int,
        limit: int
) -> list[NominationEventFullInfoSchema]:
    events_db = db.query(Event).offset(offset).limit(limit).all()
    return get_nomination_events_info_db(db, events_db)


def get_nomination_events_full_info_by_owner_db(
        db: Session,
        offset: int,
        limit: int,
        owner_id: int
) -> list[NominationEventFullInfoSchema]:

    events_db = db.query(Event). \
        filter(cast("ColumnElement[bool]", Event.owner_id == owner_id)). \
        offset(offset).limit(limit).all()

    return get_nomination_events_info_db(db, events_db)


def get_nomination_events_all_names_db(db: Session, offset: int, limit: int):
    events_db = get_all_events_db(db)
    nominations_db = get_all_nominations_db(db)
    return get_nomination_events_names_db(db, nominations_db, events_db, offset, limit)


def get_nomination_events_all_names_by_owner_db(db: Session, offset: int, limit: int, owner_id: int):
    events_db = get_all_events_by_owner_db(db, owner_id)
    nominations_db = get_all_nominations_db(db)
    return get_nomination_events_names_db(db, nominations_db, events_db, offset, limit)


def finish_event_nomination_registration_db(db: Session, nomination_name: str, event_name: str):
    event_db = db.query(Event).filter(cast("ColumnElement[bool]", Event.name == event_name)).first()
    nomination_db = db.query(Nomination). \
        filter(cast("ColumnElement[bool]", Nomination.name == nomination_name)).first()

    nomination_event_db = db.query(NominationEvent).filter(and_(
        NominationEvent.nomination_id == nomination_db.id,
        NominationEvent.event_id == event_db.id
    )
    ).first()

    nomination_event_db.registration_finished = True
    db.add(nomination_event_db)
    db.commit()


def get_nomination_events_names_db(
        db: Session,
        nominations_db: list[type(Nomination)],
        events_db: list[type(Event)],
        offset: int,
        limit: int
):
    event_id_name_pairs = {event_db.id: event_db.name for event_db in events_db}
    nomination_id_name_pairs = {nomination_db.id: nomination_db.name for nomination_db in nominations_db}

    nominations_events_db = db.query(NominationEvent). \
        filter(NominationEvent.event_id.in_(event_id_name_pairs)). \
        offset(offset).limit(limit).all()

    nomination_events = []

    for nomination_event_db in nominations_events_db:
        nomination_events.append(
            NominationEventSchema(
                event_name=event_id_name_pairs[nomination_event_db.event_id],
                nomination_name=nomination_id_name_pairs[nomination_event_db.nomination_id],
            )
        )

    return nomination_events


def delete_nomination_event_db(db: Session, nomination_event_data: NominationEventDeleteSchema):
    event_db = get_event_by_name_db(db, nomination_event_data.event_name)
    nomination_db = get_nomination_by_name_db(db, nomination_event_data.nomination_name)
    nomination_event_db = db.query(NominationEvent).\
        filter(
            and_(
                NominationEvent.event_id == event_db.id,
                NominationEvent.nomination_id == nomination_db.id,
                NominationEvent.type == nomination_event_data.type
            )
    ).first()
    db.query(TeamParticipantNominationEvent).\
        filter(TeamParticipantNominationEvent.nomination_event_id == nomination_event_db.id).all()

    db.query(TeamParticipantNominationEvent).\
        filter(TeamParticipantNominationEvent.nomination_event_id == nomination_event_db.id).delete()
    db.query(NominationEvent). \
        filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == nomination_event_data.type
        )
    ).delete()
    db.commit()
