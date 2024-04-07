from typing import cast

from pydantic import EmailStr
from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.participant import Participant
from db.models.team import Team
from db.models.team_participant import TeamParticipant
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.schemas.team_nomination_event.append_team_participant_nomination_event import \
    AppendTeamParticipantNominationEventSchema
from db.schemas.team_nomination_event.delete_team_participant_nomination_event import \
    DeleteTeamParticipantNominationEventSchema
from db.schemas.team_nomination_event.update_team_participant_nomination_event import \
    UpdateTeamParticipantNominationEventSchema


def append_team_participant_nomination_event_db(
        db: Session,
        team_participant_nomination_event_data: AppendTeamParticipantNominationEventSchema
):
    team_name = team_participant_nomination_event_data.team_name
    participant_email = team_participant_nomination_event_data.participant_email
    nomination_name = team_participant_nomination_event_data.nomination_name
    event_name = team_participant_nomination_event_data.event_name
    nomination_event_type = team_participant_nomination_event_data.nomination_event_type
    software = team_participant_nomination_event_data.software
    equipment = team_participant_nomination_event_data.equipment

    event_db = db.query(Event).\
        filter(cast("ColumnElement[bool]", Event.name == event_name)).first()
    nomination_db = db.query(Nomination).\
        filter(cast("ColumnElement[bool]", Nomination.name == nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == nomination_event_type
        )
    ).first()

    team_db = db.query(Team).\
        filter(cast("ColumnElement[bool]", Team.name == team_name)).first()
    participant_db = db.query(Participant).\
        filter(cast("ColumnElement[bool]", Participant.email == participant_email)).first()

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

    team_participant_nomination_event_db.software = software
    team_participant_nomination_event_db.equipment = equipment

    db.add(nomination_event_db)
    db.commit()


def delete_team_participant_nomination_event_db(
        db: Session,
        team_participant_nomination_event_data: DeleteTeamParticipantNominationEventSchema
):
    participant_db = db.query(Participant).\
        filter(
            cast(
                "ColumnElement[bool]", Participant.email == team_participant_nomination_event_data.participant_email
            )
    ).first()

    event_db = db.query(Event).\
        filter(
            cast(
                "ColumnElement[bool]", Event.name == team_participant_nomination_event_data.event_name
            )
    ).first()

    nomination_db = db.query(Nomination). \
        filter(
            cast(
                "ColumnElement[bool]", Nomination.name == team_participant_nomination_event_data.nomination_name
            )
    ).first()

    nomination_event_db = db.query(NominationEvent).\
        filter(
            and_(
                NominationEvent.event_id == event_db.id,
                NominationEvent.nomination_id == nomination_db.id,
                NominationEvent.type == team_participant_nomination_event_data.nomination_event_type
            )
    ).first()

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
        team_participant_nomination_event_data: UpdateTeamParticipantNominationEventSchema
):
    participant_db = db.query(Participant).\
        filter(
            cast(
                "ColumnElement[bool]", Participant.email == team_participant_nomination_event_data.participant_email
            )
    ).first()

    event_db = db.query(Event). \
        filter(
            cast(
                "ColumnElement[bool]", Event.name == team_participant_nomination_event_data.event_name
            )
    ).first()

    nomination_db = db.query(Nomination). \
        filter(
            cast(
                "ColumnElement[bool]", Nomination.name == team_participant_nomination_event_data.nomination_name
            )
    ).first()

    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == team_participant_nomination_event_data.nomination_event_type
        )
    ).first()

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
    team_participant_nomination_event_db.software = team_participant_nomination_event_data.software
    team_participant_nomination_event_db.equipment = team_participant_nomination_event_data.equipment
    db.add(team_participant_nomination_event_db)
    db.commit()
