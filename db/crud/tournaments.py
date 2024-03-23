from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.schemas.group_tournament import StartGroupTournamentSchema
from db.schemas.nomination_event import NominationEventSchema


def create_group_tournament_db(db: Session, nomination_event: StartGroupTournamentSchema):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == nomination_event.event_name)).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_event.nomination_name)).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.event_id == event_db.id,
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.type == nomination_event.type
        )
    ).first()
    nomination_event_db.tournament_started = True

    team_ids = [team_participant_db.team_id for team_participant_db in nomination_event_db.team_participants]
    print(team_ids, nomination_event.group_count)
