from typing import cast

from sqlalchemy.orm import Session

from db.crud.event import get_all_events_db, get_all_events_by_owner_db, get_events_data, get_event_by_name_db
from db.crud.nominations import get_all_nominations_db, create_nominations_missing_in_db, get_nomination_by_name_db
from db.models.event import Event
from db.models.group import Group
from db.models.group_team import GroupTeam
from db.models.match import Match
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.nominatuin_event_judge import NominationEventJudge
from db.models.participant import Participant
from db.models.team import Team
from db.models.team_participant import TeamParticipant
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.models.user import User
from db.schemas.event import EventListSchema, EventGetNameSchema
from db.schemas.nomination import NominationSchema
from db.schemas.nomination_event import NominationEventSchema, NominationEventDeleteSchema, \
    NominationEventFullInfoSchema, NominationEventParticipantCountSchema, NominationEventPDFSchema, NominationEventType, \
    OlympycNominationEventSchema
from sqlalchemy import and_

from db.schemas.participant import ParticipantPDFSchema
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
        nomination_event_data: NominationEventSchema,
        owner_id: int
):
    user_db = db.query(User).filter(cast("ColumnElement[bool]", User.id == owner_id)).first()
    nomination_db = get_nomination_by_name_db(db, nomination_event_data.nomination_name)
    event_db = get_event_by_name_db(db, nomination_event_data.event_name)
    nomination_event_db = NominationEvent(
        event_id=event_db.id,
        nomination_id=nomination_db.id,
        registration_finished=False,
        type=nomination_event_data.type
    )
    nomination_event_db.judges.append(user_db)
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

    judges_ids = set(judge_db.id for judge_db in nomination_event_db.judges)

    db.query(NominationEventJudge).filter(NominationEventJudge.judge_id.in_(judges_ids)).delete()

    for group in nomination_event_db.groups:
        for team in group.teams:
            db.query(GroupTeam).filter(and_(
                GroupTeam.tournament_group_id == group.id,
                GroupTeam.team_id == team.id
            )).delete()
        for match in group.matches:
            db.query(Match).filter(Match.id == match.id).delete()
        db.query(Group).filter(Group.id == group.id).delete()

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


def get_nomination_event_pdf_data_db(db: Session, data: list[NominationEventSchema]):

    pdf_data = []

    for i, item in enumerate(data):
        pdf_data.append(NominationEventPDFSchema(
                nomination_name=item.nomination_name,
                event_name=item.event_name,
                type=item.type,
                participants=[]

            )
        )

        event_db = db.query(Event).filter(cast("ColumnElement[bool]", Event.name == item.event_name)).first()
        nomination_db = db.query(Nomination).filter(cast("ColumnElement[bool]", Nomination.name == item.nomination_name)).first()
        nomination_event_db = db.query(NominationEvent).filter(
            and_(
               NominationEvent.event_id == event_db.id,
               NominationEvent.nomination_id == nomination_db.id,
               NominationEvent.type == item.type
            )
        ).first()
        team_participants_nominations_event_db = db.query(TeamParticipantNominationEvent).filter(
            TeamParticipantNominationEvent.nomination_event_id == nomination_event_db.id
        ).all()

        team_participant_id_software = {}
        team_participant_id_equipment = {}

        team_participant_ids = set()
        for team_participant_nomination_event_db in team_participants_nominations_event_db:
            team_participant_ids.add(team_participant_nomination_event_db.team_participant_id)
            team_participant_id_software[team_participant_nomination_event_db.team_participant_id] = team_participant_nomination_event_db.software
            team_participant_id_equipment[team_participant_nomination_event_db.team_participant_id] = team_participant_nomination_event_db.equipment

        participant_ids = set()
        participant_id_software = {}
        participant_id_equipment = {}
        for team_participant in db.query(TeamParticipant).filter(TeamParticipant.id.in_(team_participant_ids)).all():
            participant_ids.add(team_participant.participant_id)
            participant_id_software[team_participant.participant_id] = team_participant_id_software[team_participant.id]
            participant_id_equipment[team_participant.participant_id] = team_participant_id_equipment[team_participant.id]

        participants_db = [
            participant_db for participant_db  in
            db.query(Participant).filter(Participant.id.in_(participant_ids)).all()
                           ]

        [
            pdf_data[i].participants.append(
                ParticipantPDFSchema(
                    first_name=participant_db.first_name,
                    second_name=participant_db.second_name,
                    third_name=participant_db.third_name,
                    region=participant_db.region,
                    birth_date=participant_db.birth_date,
                    educational_institution=participant_db.educational_institution,
                    additional_educational_institution=participant_db.additional_educational_institution,
                    supervisor_first_name=participant_db.supervisor_first_name,
                    supervisor_second_name=participant_db.supervisor_second_name,
                    supervisor_third_name=participant_db.supervisor_third_name,
                    software=participant_id_software[participant_db.id],
                    equipment=participant_id_equipment[participant_db.id]
                )
            )
            for participant_db in participants_db
        ]
    return pdf_data


def close_registration_nomination_event_db(db: Session, nomination_event_data: OlympycNominationEventSchema):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == nomination_event_data.event_name)
    ).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_event_data.nomination_name)
    ).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == NominationEventType.olympyc
        )
    ).first()

    nomination_event_db.registration_finished = True
    db.add(nomination_event_db)
    db.commit()


def open_registration_nomination_event_db(db: Session, nomination_event_data: NominationEventSchema):
    event_db = db.query(Event).filter(cast("ColumnElement[bool]", Event.name == nomination_event_data.event_name)).first()
    nomination_db = db.query(Nomination).filter(cast("ColumnElement[bool]", Nomination.name == nomination_event_data.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == nomination_event_data.type
        )
    ).first()

    nomination_event_db.registration_finished = False
    db.add(nomination_event_db)
    db.commit()


def is_tournament_started_db(db: Session, nomination_event: OlympycNominationEventSchema):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == nomination_event.event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_event.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == NominationEventType.olympyc
        )
    ).first()
    return nomination_event_db.tournament_started


def get_judge_command_ids_db(db: Session, nomination_name: str, event_name: str, nomination_event_type: str):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == nomination_event_type
        )
    ).first()
    return set(judge_db.id for judge_db in nomination_event_db.judges).union({event_db.owner_id})


def is_group_stage_finished_db(db: Session, nomination_event: OlympycNominationEventSchema):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == nomination_event.event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_event.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == NominationEventType.olympyc
        )
    ).first()
    return nomination_event_db.group_stage_finished
