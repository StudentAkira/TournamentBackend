from sqlalchemy.orm import Session

from db.models.nomination_event import NominationEvent
from db.models.participant import Participant
from db.models.team import Team


def get_participants_of_nomination_event_db(
        db: Session,
        nomination_event_db: type(NominationEvent)
):
    participants_ids = set(participant_db.participant_id for participant_db in nomination_event_db.team_participants)
    participants_db = db.query(Participant).filter(Participant.id.in_(participants_ids))
    return participants_db


def get_participants_of_nomination_event_exclude_team_db(
        db: Session,
        team_db: Team,
        nomination_event_db: type(NominationEvent)
):
    participants_ids = set(
        team_participant_db.participant_id for team_participant_db
        in nomination_event_db.team_participants
        if team_participant_db.team_id != team_db.id
    )
    participants_db = db.query(Participant).filter(Participant.id.in_(participants_ids))
    return participants_db
