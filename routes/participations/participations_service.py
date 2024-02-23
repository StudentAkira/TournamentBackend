from db.crud import get_events_db, get_nominations_db, create_event_db
from db.schemas import Participant, Event, Nomination, Team, EventCreate
from managers.token_manager import TokenManager
from managers.user_manager import UserManager


class ParticipationsService:

    def __init__(self, db):
        self.__db = db
        self.__token_manager = TokenManager(db)
        self.__user_manager = UserManager(db)

        self.__event_created_message = "event created"

    def get_my_events(self, offset, limit) -> list[Event]:
        events = get_events_db(self.__db, offset, limit)
        return events

    def get_nominations(self, offset, limit):
        nominations = get_nominations_db(self.__db, offset, limit)
        return  nominations

    def create_event(self, token: str, event: EventCreate):
        decoded = self.__token_manager.decode_token(token)
        self.__user_manager.raise_exception_if_user_specialist(decoded.get("role"))
        create_event_db(self.__db, event, decoded.get("user_id"))
        return {"message": self.__event_created_message}

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
