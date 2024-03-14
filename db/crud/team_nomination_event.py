from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.crud.nomination_event import get_nomination_event_db
from db.crud.team import set_software_equipment_db
from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.participant import Participant
from db.models.team import Team
from db.models.team_participant import TeamParticipant
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.schemas.team_nomination_event import AppendTeamToEventNominationSchema


def append_team_to_nomination_event_db(
        db: Session,
        team_nomination_event_data: AppendTeamToEventNominationSchema
):
    team_name = team_nomination_event_data.team_name
    participant_emails = team_nomination_event_data.participant_emails
    nomination_name = team_nomination_event_data.nomination_name
    event_name = team_nomination_event_data.event_name

    team_id = db.query(Team.id).filter(
        cast("ColumnElement[bool]", Team.name == team_name)
    ).first()[0]

    participant_ids = db.query(Participant.id).filter(Participant.email.in_(set(participant_emails))).all()

    set_participant_ids = set()
    for participant_id in participant_ids:
        set_participant_ids.add(participant_id[0])

    nomination_event_db = get_nomination_event_db(db, nomination_name, event_name)

    team_participants = db.query(TeamParticipant).filter(
        and_(
            TeamParticipant.team_id == team_id,
            TeamParticipant.participant_id.in_(set_participant_ids)
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


def get_nomination_event_teams_db(db: Session, nomination_name: str, event_name: str):
    event_id = db.query(Event.id).filter(
        cast("ColumnElement[bool]", Event.name == event_name)
    ).first()[0]
    nomination_id = db.query(Nomination.id).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_name)
    ).first()[0]

    nomination_event_id = db.query(NominationEvent.id).filter(
        and_(
            NominationEvent.nomination_id == nomination_id, NominationEvent.event_id == event_id
        )
    ).first()[0]

    team_participant_ids = db.query(TeamParticipantNominationEvent.team_participant_id). \
        filter(TeamParticipantNominationEvent.nomination_event_id == nomination_event_id).all()

    set_team_participant_ids = set()
    for team_participant_id in team_participant_ids:
        set_team_participant_ids.add(team_participant_id[0])

    team_ids = set(db.query(TeamParticipant.team_id).
                   filter(TeamParticipant.id.in_(set_team_participant_ids)).all())

    set_team_ids = set()
    for team_id in team_ids:
        set_team_ids.add(team_id[0])

    teams_db = db.query(Team).filter(Team.id.in_(set_team_ids))

    return teams_db
