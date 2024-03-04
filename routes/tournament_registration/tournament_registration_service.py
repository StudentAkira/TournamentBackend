from starlette.responses import Response

from db.schemas.team import TeamSchema
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

        self.__team_appended_message = "team appended to nomination event"

    def get_teams_of_event_nomination(
            self,
            response: Response,
            token: str,
            nomination_name: str,
            event_name: str,
    ) -> list[TeamSchema]:
        decoded_token = self.__token_manager.decode_token(token, response)

        self.__event_manager.raise_exception_if_event_not_found(event_name)
        self.__nomination_manager.raise_exception_if_nomination_not_found(nomination_name)
        self.__nomination_event_manager.raise_exception_if_nomination_event_not_found(nomination_name, event_name)

        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_event_owner_wrong(event_name, decoded_token.user_id)

        return self.__nomination_event_manager.get_nomination_event_teams(nomination_name, event_name)

    def append_team_to_event_nomination(#long method; refactor todo
            self,
            response: Response,
            token: str,
            team_name: str,
            nomination_name: str,
            event_name: str,
    ):
        decoded_token = self.__token_manager.decode_token(token, response)

        self.__team_manager.raise_exception_if_team_not_found(team_name)
        self.__event_manager.raise_exception_if_event_not_found(event_name)
        self.__nomination_manager.raise_exception_if_nomination_not_found(nomination_name)
        self.__nomination_event_manager.raise_exception_if_nomination_event_not_found(nomination_name, event_name)

        if decoded_token.role == UserRole.specialist or decoded_token.role == UserRole.judge:
            self.__team_manager.raise_exception_if_team_owner_wrong(team_name, decoded_token.user_id)
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_event_owner_wrong(event_name, decoded_token.user_id)

        self.__nomination_event_manager.raise_exception_if_team_already_in_nomination_event(
            team_name,
            nomination_name,
            event_name
        )

        self.__nomination_event_manager.raise_exception_if_participant_already_in_event_nomination(
            team_name,
            nomination_name,
            event_name
        )

        self.__nomination_event_manager.append_team_to_event_nomination(team_name, nomination_name, event_name)

        return {"message": self.__team_appended_message}

    def get_nomination_events(self, offset, limit, response, token):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__nomination_event_manager.get_events_nominations(offset, limit, decoded_token.user_id)