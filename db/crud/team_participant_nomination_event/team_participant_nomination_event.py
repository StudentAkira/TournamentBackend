from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.nomination_event import NominationEvent
from db.models.participant import Participant
from db.models.team import Team
from db.models.team_participant import TeamParticipant
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.schemas.team_nomination_event.append_team_participant_nomination_event import \
    AppendTeamParticipantNominationEventSchema
from db.schemas.team_nomination_event.update_team_participant_nomination_event import \
    UpdateTeamParticipantNominationEventSchema


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
