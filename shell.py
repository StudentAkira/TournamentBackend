import os
from io import BytesIO

from fpdf import FPDF
from fpdf.enums import PageMode
from reportlab.pdfgen import canvas

from db.database import *
from sqlalchemy import and_
from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.participant import Participant
from db.models.team import Team
from db.models.team_participant import TeamParticipant
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.models.token import Token
from db.models.user import User
from db.schemas.user import UserSchema


from db.models.nominatuin_event_judge import NominationEventJudge
from db.models.match import Match
from db.models.group import Group
from db.models.bracket import Bracket
from db.models.group_team import GroupTeam
from db.models.bracket_team import BracketTeam

db = SessionLocal()


def counting_sort(arr):
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    sorted_arr = []
    for i in range(len(count)):
        sorted_arr.extend([i] * count[i])
    return sorted_arr
