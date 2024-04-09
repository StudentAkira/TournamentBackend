from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from config import get_settings
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
from fastapi.testclient import TestClient
from main import app

settings = get_settings()


SQLALCHEMY_DATABASE_URL =f"{settings.db}://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
)

Session = sessionmaker(bind=engine)
db = Session()

