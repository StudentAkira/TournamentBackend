from db.crud import get_events_db
from db.schemas import Participant, Event, Nomination, Team
from managers.token_manager import TokenManager
from managers.user_manager import UserManager


class ParticipationsService:

    def __init__(self, db):
        self.__db = db
        self.__token_manager = TokenManager(db)
        self.__user_manager = UserManager(db)

    def get_my_events(self, start, limit) -> list[Event]:
        events = get_events_db(self.__db, start, limit)
        return events

    def get_nominations(self, start, limit):
        pass

    def create_event(self, token: str, event: Event, nominations: list[Nomination] | None = None):
        pass

    def create_nominations(self, token: str, nominations: list[Nomination]):
        pass

    def specify_nominations_for_event(self, token: str, event: Event, nominations: list[Nomination]):
        pass

    def create_team(self, token: str, team: Team):
        pass

    def create_participant(self, token: str, participant: Participant, teams: list[Team] | None = None):
        pass

    def specify_teams_for_participant(self, token: str, teams: list[Team], participant: Participant):
        pass
