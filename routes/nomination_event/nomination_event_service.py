from starlette.responses import Response
from db.schemas.nomination_event import NominationEventDeleteSchema, NominationEventSchema
from db.schemas.user import UserRole
from managers.event import EventManager
from managers.nomination import NominationManager
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
        self.__nomination_manager = NominationManager(db)

        self.__nominations_appended_message = "nomination appended"
        self.__nomination_event_deleted_message = "nomination event deleted"
        self.__registration_closed_message = "registration closed"
        self.__registration_opened_message = "registration opened"

    def get_nomination_event_pdf(self, response: Response, token: str, data: list[NominationEventSchema]):
        decoded_token = self.__token_manager.decode_token(token, response)

        for item in data:
            self.__event_manager.raise_exception_if_not_found(item.event_name)
            self.__nomination_manager.raise_exception_if_not_found(item.nomination_name)
            self.__nomination_event_manager.raise_exception_if_not_found(
                item.nomination_name,
                item.event_name,
                item.type
            )

            self.__event_manager.raise_exception_if_owner_wrong(item.event_name, decoded_token.user_id)

        return self.__nomination_event_manager.get_nomination_event_pdf(data)

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

    def append_nomination_for_event(
            self,
            response: Response,
            token: str,
            nomination_event_data: NominationEventSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)

        self.__event_manager.raise_exception_if_not_found(nomination_event_data.event_name)
        self.__nomination_manager.raise_exception_if_not_found(nomination_event_data.nomination_name)

        self.__nomination_event_manager.raise_exception_if_exists(
            nomination_event_data
        )
        self.__nomination_event_manager.append(nomination_event_data, decoded_token.user_id)
        return {"message": self.__nominations_appended_message}

    def get_nomination_event_data(
            self,
            response: Response,
            token: str,
            event_name: str
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__event_manager.raise_exception_if_not_found(event_name)
        return self.__nomination_event_manager.get_nomination_event_data(event_name)

    def delete(self, response: Response, token: str, nomination_event_data: NominationEventDeleteSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__event_manager.raise_exception_if_not_found(nomination_event_data.event_name)
        self.__nomination_manager.raise_exception_if_not_found(nomination_event_data.nomination_name)
        self.__nomination_event_manager.raise_exception_if_not_found(
            nomination_event_data.nomination_name,
            nomination_event_data.event_name,
            nomination_event_data.type
        )
        self.__event_manager.raise_exception_if_owner_wrong(nomination_event_data.event_name, decoded_token.user_id)
        self.__nomination_event_manager.delete(nomination_event_data)
        return {"message": self.__nomination_event_deleted_message}

    def close_registration(
            self,
            response: Response,
            token: str,
            nomination_event_data: NominationEventSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__validator.check_event_nomination__nomination_event_existence(
            nomination_event_data.nomination_name,
            nomination_event_data.event_name,
            nomination_event_data.type
        )
        self.__event_manager.raise_exception_if_owner_wrong(nomination_event_data.event_name, decoded_token.user_id)
        self.__nomination_event_manager.close_registration(nomination_event_data)
        self.__nomination_event_manager.raise_exception_if_tournament_started(
            nomination_event_data.nomination_name,
            nomination_event_data.event_name,
            nomination_event_data.type
        )
        return {"message": self.__registration_closed_message}

    def open_registration(
            self,
            response: Response,
            token: str,
            nomination_event_data: NominationEventSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__validator.check_event_nomination__nomination_event_existence(
            nomination_event_data.nomination_name,
            nomination_event_data.event_name,
            nomination_event_data.type
        )
        self.__event_manager.raise_exception_if_owner_wrong(nomination_event_data.event_name, decoded_token.user_id)
        self.__nomination_event_manager.raise_exception_if_tournament_started(
            nomination_event_data.nomination_name,
            nomination_event_data.event_name,
            nomination_event_data.type
        )
        self.__nomination_event_manager.open_registration(nomination_event_data)
        return {"message": self.__registration_opened_message}
