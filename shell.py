from typing import cast
from db.database import *
from sqlalchemy import and_
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
from db.schemas.group_tournament import GetGroupsOfTournamentSchema, GroupSchema
from db.schemas.participant import ParticipantSchema
from db.schemas.team_participant import TeamParticipantsSchema

db = SessionLocal()


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)



