from starlette.responses import Response

from db.schemas.nomination_event import NominationEventNameSchema, NominationEventSchema
from db.schemas.team import TeamSchema
from db.schemas.user import UserRole
from managers.event_manager import EventManager
from managers.nomination_event_manager import NominationEventManager
from managers.token_manager import TokenManager
from validators.validator import Validator


class NominationEventService:
    def __init__(self, db):
        self.__event_manager = EventManager(db)
        self.__validator = Validator(db)
        self.__token_manager = TokenManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__db = db

    def get_list_events_list_nominations(self, response: Response, token: str):
        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role == UserRole.judge:
            return self.__nomination_event_manager.get_list_events_list_nominations_by_owner(decoded_token.owner_id)
        return self.__nomination_event_manager.get_list_events_list_nominations()

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

    def get_teams_of_nomination_event(
            self,
            response: Response,
            token: str,
            nomination_name: str,
            event_name: str,
    ) -> list[TeamSchema]:
        decoded_token = self.__token_manager.decode_token(token, response)

        self.__validator.check_event_nomination__nomination_event_existence(nomination_name, event_name)
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_event_owner_wrong(event_name, decoded_token.user_id)

        return self.__nomination_event_manager.get_teams_of_nomination_event(nomination_name, event_name)
