from starlette.responses import Response

from db.schemas.event import EventSchema
from db.schemas.user import UserRole
from managers.event import EventManager
from managers.nomination_event import NominationEventManager
from managers.team_nomination_event import TeamNominationEventManager
from managers.token import TokenManager
from managers.user import UserManager
from validators.validator import Validator


class NominationEventService:
    def __init__(self, db):
        self.__db = db

        self.__team_nomination_event_manager = TeamNominationEventManager(db)
        self.__event_manager = EventManager(db)
        self.__validator = Validator(db)
        self.__token_manager = TokenManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__user_manager = UserManager(db)

        self.__nominations_appended_message = "nomination appended"

    def list(self, response: Response, token: str, offset: int, limit: int):
        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role == UserRole.judge:
            return self.__nomination_event_manager.list_by_owner(offset, limit, decoded_token.owner_di)
        return self.__nomination_event_manager.list(offset, limit)

    def get_nomination_events_names(
            self,
            response: Response,
            token: str,
            offset: int,
            limit: int
    ) -> list:
        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role != UserRole.judge:
            return self.__nomination_event_manager.list(offset, limit)
        return self.__nomination_event_manager.list_by_owner(
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
    ) -> list:
        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role != UserRole.judge:
            return self.__nomination_event_manager.list_full_info(offset, limit)
        return self.__nomination_event_manager.list_full_info_by_owner(
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
    ) -> list:
        decoded_token = self.__token_manager.decode_token(token, response)

        self.__validator.check_event_nomination__nomination_event_existence(nomination_name, event_name)
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_owner_wrong(event_name, decoded_token.user_id)

        return self.__team_nomination_event_manager.list_teams_of_nomination_event(nomination_name, event_name)

    def append_nominations_for_event(
            self,
            response: Response,
            token: str,
            event: EventSchema,
            nominations: list
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        self.__event_manager.raise_exception_if_not_found(event.name)
        self.__nomination_event_manager.append_many(event, nominations)
        return {"message": self.__nominations_appended_message}
