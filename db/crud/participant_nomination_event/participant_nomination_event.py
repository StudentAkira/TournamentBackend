from sqlalchemy.orm import Session

from db.models.nomination_event import NominationEvent
from db.models.participant import Participant


def get_participants_of_nomination_event_db(
        db: Session,
        nomination_event_db: type(NominationEvent)
):
    participants_ids = set(participant_db.participant_id for participant_db in nomination_event_db.team_participants)
    participants_db = db.query(Participant).filter(Participant.id.in_(participants_ids))
    return participants_db
