from typing import cast
from sqlalchemy import and_
from sqlalchemy.orm import Session
from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.team import Team
from db.models.team_participant import TeamParticipant
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.schemas.nomination_event.nomination_event import NominationEventSchema


def get_nomination_event_teams_db(db: Session, nomination_event_db: type(NominationEvent)):
    team_participant_ids = db.query(TeamParticipantNominationEvent.team_participant_id). \
        filter(
        TeamParticipantNominationEvent.nomination_event_id == nomination_event_db.id
    ).all()

    set_team_participant_ids = set()
    for team_participant_id in team_participant_ids:
        set_team_participant_ids.add(team_participant_id[0])
    team_ids = set(
        team_id[0]
        for team_id in
            db.query(TeamParticipant.team_id).
                       filter(TeamParticipant.id.in_(set_team_participant_ids)).all()
        )
    teams_db = db.query(Team).filter(Team.id.in_(team_ids))
    return teams_db
