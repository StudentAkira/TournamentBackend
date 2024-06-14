from typing import cast
from db.database import *
from sqlalchemy import and_, not_
from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from itertools import combinations


from db.models.user import User
from db.models.group import Group
from db.models.bracket import Bracket
from db.models.nominatuin_event_judge import NominationEventJudge
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.models.team_participant import TeamParticipant
from db.models.token import Token
from db.models.team import Team
from db.models.participant import Participant
from db.models.group import Group
from db.models.group_team import GroupTeam
from db.models.bracket_team import BracketTeam
from db.models.match import Match
from db.models.race_round import RaceRound
from db.schemas.event.event import EventSchema
from db.schemas.event.event_by_id import EventByIdSchema
from db.schemas.event.event_list import EventListSchema
from db.schemas.nomination.nomination import NominationSchema

from db.schemas.nomination_event.nomination_event_type import NominationEventType

db = SessionLocal()

teams_db = db.query(Team).filter(and_(
        cast("ColumnElement[bool]", Team.creator_id == 1),
        cast("ColumnElement[bool]", not_(Team.name.ilike("%@%")))
        )
    ).all()
