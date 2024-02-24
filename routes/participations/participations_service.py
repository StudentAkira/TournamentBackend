from db.crud import get_events_db, get_nominations_db, create_event_db
from db.schemas import Participant, Event, Team, EventCreate, BaseNomination
from managers.event_manager import EventManager
from managers.nomination_manager import NominationManager
from managers.paticipant_manager import ParticipantManager
from managers.team_manager import TeamManager
from managers.token_manager import TokenManager
from managers.user_manager import UserManager


class ParticipationsService:

    def __init__(self, db):
        self.__db = db
        self.__token_manager = TokenManager(db)
        self.__user_manager = UserManager(db)
        self.__event_manager = EventManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__team_manager = TeamManager(db)
        self.__participant_manager = ParticipantManager(db)

    def get_my_events(self, offset, limit) -> list[Event]:
        events = get_events_db(self.__db, offset, limit)
        return events

    def get_nominations(self, offset, limit):
        nominations = self.__nomination_manager.get_nominations(offset, limit)
        return nominations

    def create_event(self, token: str, event: EventCreate):
        decoded = self.__token_manager.decode_token(token)
        self.__user_manager.raise_exception_if_user_specialist(decoded.get("role"))
        return self.__event_manager.create_event(event, decoded.get("user_id"))

    def create_nominations(self, token: str, nominations: list[BaseNomination]):
        decoded = self.__token_manager.decode_token(token)
        self.__user_manager.raise_exception_if_user_specialist(decoded.get("role"))
        return self.__nomination_manager.create_nominations(nominations)

    def append_nominations_for_event(self, token: str, event: Event, nominations: list[BaseNomination]):
        decoded = self.__token_manager.decode_token(token)
        self.__user_manager.raise_exception_if_user_specialist(decoded.get("role"))
        event = self.__event_manager.get_event_by_name(event.name)
        self.__event_manager.raise_exception_if_event_dont_exist(event)
        return self.__event_manager.append_nominations(event, nominations)

    def create_team(self, token: str, team: Team):
        pass

    def create_participant(self, token: str, participant: Participant, teams: list[Team] | None = None):
        pass

    def specify_teams_for_participant(self, token: str, teams: list[Team], participant: Participant):
        pass
