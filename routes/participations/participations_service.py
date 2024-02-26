from starlette.responses import Response

from db.crud import get_events_db, get_my_events_db
from db.schemas import Participant, Event, Team, EventCreate, BaseNomination, Software, Equipment, UserRole
from managers.equipment_manager import EquipmentManager
from managers.event_manager import EventManager
from managers.nomination_event_manager import NominationEventManager
from managers.nomination_manager import NominationManager
from managers.paticipant_manager import ParticipantManager
from managers.software_manager import SoftwareManager
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
        self.__software_manager = SoftwareManager(db)
        self.__equipment_manager = EquipmentManager(db)
        self.__nomination_event_manager = NominationEventManager(db)

    def get_events(self, offset, limit) -> list[Event]:
        events = get_events_db(self.__db, offset, limit)
        return events

    def get_my_events(self,response: Response, token: str, offset, limit) -> list[Event]:
        decoded = self.__token_manager.decode_token(token, response)
        events = []
        if decoded.get("role") == UserRole.specialist or decoded.get("role") == UserRole.admin:
            events = self.get_events(offset, limit)
        if decoded.get("role") == UserRole.judge:
            events = get_my_events_db(self.__db, offset, limit, decoded.get("user_id"))
        return events

    def get_nominations(self, offset, limit):
        nominations = self.__nomination_manager.get_nominations(offset, limit)
        return nominations

    def create_event(self, response: Response, token: str, event: EventCreate):
        decoded = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded.get("role"))
        return self.__event_manager.create_event(event, decoded.get("user_id"))

    def create_nominations(self,  response: Response, token: str, nominations: list[BaseNomination]):
        decoded = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded.get("role"))
        return self.__nomination_manager.create_nominations(nominations)

    def append_nominations_for_event(self, response: Response, token: str, event: Event, nominations: list[BaseNomination]):
        decoded = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded.get("role"))
        self.__event_manager.raise_exception_if_event_dont_exist(event.name)
        return self.__event_manager.append_nominations(event, nominations)

    def create_team(self, response, token: str, team: Team):
        decoded = self.__token_manager.decode_token(token, response)
        return self.__team_manager.create_team(team, decoded.get("user_id"))

    def get_my_teams(self, response, token, offset: int, limit: int):
        decoded = self.__token_manager.decode_token(token, response)
        return self.__team_manager.get_my_teams(offset, limit, decoded.get("user_id"))

    def get_my_participants(self, response: Response, token: str, offset: int, limit: int):
        decoded = self.__token_manager.decode_token(token, response)
        return self.__participant_manager.get_my_participants(decoded.get("user_id"), offset, limit)

    def create_participant(self, response: Response, token: str, participant: Participant):
        decoded = self.__token_manager.decode_token(token, response)
        return self.__participant_manager.create_participant(participant, decoded.get("user_id"))

    def create_software(self, response: Response, token: str, software: list[Software]):
        self.__token_manager.decode_token(token, response)
        return self.__software_manager.create_software(software)

    def create_equipment(self, response: Response, token: str, equipment: list[Equipment]):
        self.__token_manager.decode_token(token, response)
        return self.__equipment_manager.create_equipment(equipment)

    def get_software(self, response: Response, offset: int, limit: int, token: str):
        self.__token_manager.decode_token(token, response)
        return self.__software_manager.get_softwares(offset, limit)

    def get_equipment(self, response: Response, offset: int, limit: int, token: str):
        self.__token_manager.decode_token(token, response)
        return self.__equipment_manager.get_equipment(offset, limit)

    def append_team_to_event_nomination(self, response: Response, token: str, team_name: str, event_name: str, nomination_name: str):
        self.__team_manager.raise_exception_if_team_dont_exist(team_name)
        self.__event_manager.raise_exception_if_event_dont_exist(event_name)
        self.__nomination_manager.raise_exception_if_nomination_does_not_exist(nomination_name)
        self.__nomination_event_manager.raise_exception_if_nomination_event_does_not_exist(event_name, nomination_name)

        decoded = self.__token_manager.decode_token(token, response)
        if decoded.get("role") == UserRole.admin:
            return self.__team_manager.append_team_to_event_nomination(team_name, event_name, nomination_name)
        self.__team_manager.raise_exception_if_team_owner_wrong(team_name, decoded.get("user_id"))
        if decoded.get("role") == UserRole.judge:
            self.__event_manager.raise_exception_if_event_owner_wrong(event_name, decoded.get("user_id"))
        return self.__team_manager.append_team_to_event_nomination(team_name, event_name, nomination_name)





    def append_teams_for_participant(self, response: Response, token: str, teams: list[Team], participant: Participant):
        pass

    def append_participants_for_team(self, response: Response, token: str, teams: Team, participant: list[Participant]):
        pass

