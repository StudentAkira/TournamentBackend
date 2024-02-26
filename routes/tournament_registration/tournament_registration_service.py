from starlette.responses import Response

from db.schemas.user import UserRole
from managers.event_manager import EventManager
from managers.nomination_event_manager import NominationEventManager
from managers.nomination_manager import NominationManager
from managers.team_manager import TeamManager
from managers.token_manager import TokenManager


class TournamentRegistrationService:
    def __init__(self, db):
        self.__db = db

        self.__event_manager = EventManager(db)
        self.__token_manager = TokenManager(db)
        self.__team_manager = TeamManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__nomination_manager = NominationManager(db)

    def append_team_to_event_nomination(
            self,
            response: Response,
            token: str,
            team_name: str,
            event_name: str,
            nomination_name: str
    ):
        self.__team_manager.raise_exception_if_team_dont_exist(team_name)
        self.__event_manager.raise_exception_if_event_dont_exist(event_name)
        self.__nomination_manager.raise_exception_if_nomination_does_not_exist(nomination_name)
        self.__nomination_event_manager.raise_exception_if_nomination_event_does_not_exist(event_name, nomination_name)

        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role == UserRole.admin:
            return self.__team_manager.append_team_to_event_nomination(team_name, event_name, nomination_name)
        self.__team_manager.raise_exception_if_team_owner_wrong(team_name, decoded_token.user_id)
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_event_owner_wrong(event_name, decoded_token.user_id)
        return self.__team_manager.append_team_to_event_nomination(team_name, event_name, nomination_name)
