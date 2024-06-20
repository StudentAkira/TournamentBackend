from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.crud.event.event import get_event_by_id_db
from db.crud.nomination_event.nomination_event import get_nomination_event_db
from db.models.equipment import Equipment
from db.models.nomination_event import NominationEvent
from db.models.participant import Participant
from db.models.software import Software
from db.models.team import Team
from db.models.team_participant import TeamParticipant
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.schemas.team_nomination_event.append_team_participant_nomination_event import \
    AppendTeamParticipantNominationEventSchema
from db.schemas.team_nomination_event.update_team_participant_nomination_event import \
    UpdateTeamParticipantNominationEventSchema
from db.schemas.team_participant_nomination_event.append_teams_participants_nomination_event import \
    TeamParticipantNominationEventAppendSchema


def append_team_participant_nomination_event_db(
        db: Session,
        nomination_event_db: type(NominationEvent),
        participant_db: type(Participant),
        team_db: type(Team),
        team_participant_nomination_event: AppendTeamParticipantNominationEventSchema
):
    team_participant_db = db.query(TeamParticipant).filter(
        and_(
            TeamParticipant.team_id == team_db.id,
            TeamParticipant.participant_id == participant_db.id
        )
    ).first()
    nomination_event_db.team_participants.append(team_participant_db)
    db.add(nomination_event_db)
    db.commit()
    team_participant_nomination_event_db = db.query(TeamParticipantNominationEvent).filter(
        and_(
            TeamParticipantNominationEvent.team_participant_id == team_participant_db.id,
            TeamParticipantNominationEvent.nomination_event_id == nomination_event_db.id
        )
    ).first()
    team_participant_nomination_event_db.software = team_participant_nomination_event.software
    team_participant_nomination_event_db.equipment = team_participant_nomination_event.equipment
    db.add(nomination_event_db)
    db.commit()


def delete_team_participant_nomination_event_db(
        db: Session,
        nomination_event_db: type(NominationEvent),
        participant_db: type(Participant),
):
    team_participant_id = [team_participant_db.id
                           for team_participant_db in
                           nomination_event_db.team_participants
                           if team_participant_db.participant_id == participant_db.id
                           ][0]
    db.query(TeamParticipantNominationEvent).filter(
        and_(
            TeamParticipantNominationEvent.nomination_event_id == nomination_event_db.id,
            TeamParticipantNominationEvent.team_participant_id == team_participant_id
        )
    ).delete()
    db.commit()


def update_team_participant_nomination_event_db(
        db: Session,
        nomination_event_db: type(NominationEvent),
        participant_db: type(Participant),
        team_participant_nomination_event: UpdateTeamParticipantNominationEventSchema
):
    team_participant_id = [team_participant_db.id
                           for team_participant_db in
                           nomination_event_db.team_participants
                           if team_participant_db.participant_id == participant_db.id
                           ][0]
    team_participant_nomination_event_db = db.query(TeamParticipantNominationEvent).filter(
        and_(
            TeamParticipantNominationEvent.nomination_event_id == nomination_event_db.id,
            TeamParticipantNominationEvent.team_participant_id == team_participant_id
        )
    ).first()
    team_participant_nomination_event_db.software = team_participant_nomination_event.software
    team_participant_nomination_event_db.equipment = team_participant_nomination_event.equipment
    db.add(team_participant_nomination_event_db)
    db.commit()


def refresh_db(
        db: Session,
        nomination_event_db: NominationEvent,
        team_participant_nomination_event: TeamParticipantNominationEventAppendSchema
):
    team_participants_db = []
    team_db = db.query(Team).filter(Team.id == team_participant_nomination_event.team_id).first()

    for tp in team_participant_nomination_event.team_participants:

        team_participant_db = db.query(TeamParticipant).filter(
            and_(
                TeamParticipant.team_id == team_participant_nomination_event.team_id,
                TeamParticipant.participant_id == tp.participant_id
            )
        ).first()
        team_participants_db.append(team_participant_db)
        team_participant_nomination_event_db = db.query(TeamParticipantNominationEvent).filter(
            and_(
                TeamParticipantNominationEvent.team_participant_id == team_participant_db.id,
                TeamParticipantNominationEvent.nomination_event_id == nomination_event_db.id
            )
        ).first()
        if team_participant_nomination_event_db is None:
            team_participant_nomination_event_db = TeamParticipantNominationEvent(
                team_participant_id=team_participant_db.id,
                nomination_event_id=nomination_event_db.id,
                softwares=[],
                equipments=[]
            )
        db.add(team_participant_nomination_event_db)

        team_participant_nomination_event_db.softwares.clear()
        for software in tp.softwares:
            software_db = db.query(Software).\
                filter(cast("ColumnElement[bool]", Software.software == software.name)).first()
            if software_db is None:
                software_db = Software(
                    software=software.name
                )
                db.add(software_db)
                db.commit()
            team_participant_nomination_event_db.softwares.append(software_db)

        team_participant_nomination_event_db.equipments.clear()
        for equipment in tp.equipments:
            equipment_db = db.query(Equipment).\
                filter(cast("ColumnElement[bool]", Equipment.equipment == equipment.name)).first()
            if equipment_db is None:
                equipment_db = Equipment(
                    equipment=equipment.name
                )
                db.add(equipment_db)
                db.commit()
            team_participant_nomination_event_db.equipments.append(equipment_db)
        db.add(team_participant_db)
    db.commit()

    participants_of_team_in_nomination_event_db = db.query(TeamParticipantNominationEvent).filter(
        and_(
            TeamParticipantNominationEvent.nomination_event_id == nomination_event_db.nomination_id,
            TeamParticipantNominationEvent.team_participant_id.in_(
                [
                    team_participant_db.id for team_participant_db in
                    nomination_event_db.team_participants if team_participant_db.team_id == team_db.id
                ]
            )
        )
    ).all()
    for tp in participants_of_team_in_nomination_event_db:
        if tp not in team_participants_db:
            db.delete(tp)
    db.commit()









