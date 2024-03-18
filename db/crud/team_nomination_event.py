from typing import cast
from sqlalchemy import and_
from sqlalchemy.orm import Session
from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.team import Team
from db.models.team_participant import TeamParticipant
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent


def get_nomination_event_teams_db(db: Session, nomination_name: str, event_name: str, nomination_event_type: str):
    event_db = db.query(Event).filter(
        cast("ColumnElement[bool]", Event.name == event_name)
    ).first()
    nomination_db = db.query(Nomination).filter(
        cast("ColumnElement[bool]", Nomination.name == nomination_name)
    ).first()
    nomination_event_db = db.query(NominationEvent).filter(
        and_(
            NominationEvent.nomination_id == nomination_db.id,
            NominationEvent.event_id == event_db.id,
            NominationEvent.type == nomination_event_type
        )
    ).first()

    team_participant_ids = db.query(TeamParticipantNominationEvent.team_participant_id). \
        filter(
        TeamParticipantNominationEvent.nomination_event_id == nomination_event_db.id
    ).all()

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
