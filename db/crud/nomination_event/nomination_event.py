from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.crud.event.event import get_all_events_by_owner_db, get_all_events_db
from db.crud.nomination.nomination import get_all_nominations_db
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
from db.schemas.nomination_event.nomination_event import NominationEventSchema
from db.schemas.nomination_event.nomination_event_full_info_schema import NominationEventFullInfoSchema
from db.schemas.nomination_event.nomination_event_participant_count import NominationEventParticipantCountSchema
from db.schemas.nomination_event.nomination_event_pdf import NominationEventPDFSchema
from db.schemas.nomination_event.nomination_event_type import NominationEventType
from db.schemas.participant.participant_pdf import ParticipantPDFSchema
from db.schemas.team_participant.team_participant import TeamParticipantsSchema


def get_nominations_event_participant_count_db(
        db: Session,
        event_db: type(Event)
) -> list[NominationEventParticipantCountSchema]:

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


def append_event_nomination_db(
        db: Session,
        nomination_db: type(Nomination),
        event_db: type(Event),
        user_db: type(User),
        nomination_event: NominationEventSchema
):
    nomination_event_db = NominationEvent(
        event_id=event_db.id,
        nomination_id=nomination_db.id,
        registration_finished=False,
        type=nomination_event.type,
        race_round_length=nomination_event.race_round_length if nomination_event.race_round_length else None
    )
    nomination_event_db.judges.append(user_db)
    db.add(nomination_event_db)
    db.commit()
    db.refresh(event_db)


def get_nomination_event_db(
        db: Session,
        nomination_db: type(Nomination),
        event_db: type(Event),
        type_: NominationEventType
) -> type(NominationEvent) | None:
    nomination_event_db = db.query(NominationEvent). \
        filter(and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == type_
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


def delete_nomination_event_db(db: Session, nomination_event_db: type(NominationEvent)):

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
    db.commit()
    db.delete(nomination_event_db)
    db.commit()


def get_nomination_event_pdf_data_db(db: Session, data: list[type(Nomination), type(Event), type(NominationEvent)]):

    pdf_data = []

    for i, item in enumerate(data):
        pdf_data.append(NominationEventPDFSchema(
                nomination_name=item[0].name,
                event_name=item[1].name,
                type=item[2].type,
                participants=[]
            )
        )
        team_participants_nominations_event_db = db.query(TeamParticipantNominationEvent).filter(
            TeamParticipantNominationEvent.nomination_event_id == item[2].id
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


def close_registration_nomination_event_db(db: Session, nomination_event_db: type(NominationEvent)):
    nomination_event_db.registration_finished = True
    db.add(nomination_event_db)
    db.commit()


def open_registration_nomination_event_db(db: Session, nomination_event_db: type(NominationEvent)):
    nomination_event_db.registration_finished = False
    db.add(nomination_event_db)
    db.commit()


def get_judge_command_ids_db(nomination_event_db: type(NominationEvent)):
    return set(judge_db.id for judge_db in nomination_event_db.judges)
