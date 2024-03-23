from typing import cast

from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.schemas.group_tournament import GroupMatchSchema
from db.schemas.match import MatchSchema
from db.schemas.nomination_event import NominationEventSchema
from db.schemas.team import TeamSchema


def get_group_matches_of_tournament_db(db: Session, nomination_event: NominationEventSchema):
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

    groups = [
        GroupMatchSchema(
            group_id=group_db.id,
            matches=[
                MatchSchema(
                    match_id=match_db.id,
                    team1=TeamSchema(name=match_db.team1.name) if match_db.team1 else None,
                    team2=TeamSchema(name=match_db.team2.name) if match_db.team2 else None,
                    winner=TeamSchema(name=match_db.winner.name) if match_db.winner else None,
                    match_queue_number=match_db.match_queue_number
                ) for match_db in group_db.matches
            ]
        ) for group_db in nomination_event_db.groups
    ]
    return groups
