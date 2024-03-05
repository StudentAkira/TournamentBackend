from starlette.responses import Response

from db.schemas.nomination_event import NominationEventSchema, NominationEventNameSchema
from db.schemas.team import TeamSchema
from db.schemas.token import TokenDecodedSchema
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

    def get_teams_of_nomination_event(
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

        return self.__nomination_event_manager.get_teams_of_nomination_event(nomination_name, event_name)

    def append_team_to_event_nomination(
            self,
            response: Response,
            token: str,
            team_name: str,
            nomination_name: str,
            event_name: str,
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.check_entities_existence(team_name, nomination_name, event_name)
        self.validate_user_entity_ownership(decoded_token, team_name, event_name)
        self.check_participant_team_relation_existence(team_name, nomination_name, event_name)

        self.__nomination_event_manager.append_team_to_event_nomination(team_name, nomination_name, event_name)
        return {"message": self.__team_appended_message}

    def check_participant_team_relation_existence(self, team_name: str, nomination_name: str, event_name: str):
        self.__nomination_event_manager.raise_exception_if_team_already_in_nomination_event(
            team_name,
            nomination_name,
            event_name
        )
        self.__nomination_event_manager.raise_exception_if_participant_already_in_nomination_event(
            team_name,
            nomination_name,
            event_name
        )

    def check_entities_existence(self,
                                 team_name: str,
                                 nomination_name: str,
                                 event_name: str
                                 ):
        self.__team_manager.raise_exception_if_team_not_found(team_name)
        self.__event_manager.raise_exception_if_event_not_found(event_name)
        self.__nomination_manager.raise_exception_if_nomination_not_found(nomination_name)
        self.__nomination_event_manager.raise_exception_if_nomination_event_not_found(nomination_name, event_name)

    def validate_user_entity_ownership(self, decoded_token: TokenDecodedSchema, team_name: str, event_name: str):
        if decoded_token.role == UserRole.specialist or decoded_token.role == UserRole.judge:
            self.__team_manager.raise_exception_if_team_owner_wrong(team_name, decoded_token.user_id)
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_event_owner_wrong(event_name, decoded_token.user_id)

    def get_nomination_events_full_info(
            self,
            response: Response,
            token: str,
            offset: int,
            limit: int
    ) -> list[NominationEventSchema]:
        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role != UserRole.judge:
            return self.__nomination_event_manager.get_nominations_events_full_info(offset, limit)
        return self.__nomination_event_manager.get_nominations_events_full_info_by_owner(
            offset,
            limit,
            decoded_token.user_id
        )

    def get_nomination_events_names(
            self,
            response: Response,
            token: str,
            offset: int,
            limit: int
    ) -> list[NominationEventNameSchema]:
        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role != UserRole.judge:
            return self.__nomination_event_manager.get_nominations_events_names(offset, limit)
        return self.__nomination_event_manager.get_nominations_events_names_by_owner(
            offset,
            limit,
            decoded_token.user_id
        )
