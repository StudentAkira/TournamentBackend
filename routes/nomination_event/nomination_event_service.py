from starlette.responses import Response

from db.schemas.nomination_event.nomination_event import NominationEventSchema
from db.schemas.nomination_event.nomination_event_type import NominationEventType
from db.schemas.nomination_event.nomination_eventappend import NominationEventAppendSchema
from db.schemas.user.user_role import UserRole
from managers.event import EventManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.team_nomination_event import TeamNominationEventManager
from managers.token import TokenManager
from managers.user import UserManager
from utils.validation_util import Validator


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

        data_db = []

        for item in data:
            event_db = self.__event_manager.get_by_name_or_raise_if_not_found(item.event_name)
            nomination_db = self.__nomination_manager.get_by_name_and_user_id_or_raise_exception_if_not_found(
                decoded_token.user_id,
                item.nomination_name
            )
            nomination_event_db = self.__nomination_event_manager.get_nomination_event_or_raise_if_not_found(
                nomination_db,
                event_db,
                item.type
            )
            data_db.append((nomination_db, event_db, nomination_event_db))
            self.__event_manager.raise_exception_if_owner_wrong(event_db, decoded_token.user_id)

        return self.__nomination_event_manager.get_nomination_event_pdf(data_db)

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
            nomination_event: NominationEventAppendSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        user_db = self.__user_manager.get_user_by_id_or_raise_if_not_found(decoded_token.user_id)

        event_db = self.__event_manager.get_by_id_or_raise_if_not_found(nomination_event.event_id)
        nomination_db = self.__nomination_manager.get_or_create(
            decoded_token.user_id,
            nomination_event.nomination_name
        )
        self.__nomination_event_manager.raise_exception_if_exists(
            event_db,
            nomination_db,
            nomination_event.type
        )
        if nomination_event.type == NominationEventType.time:
            self.__nomination_event_manager.raise_exception_if_nomination_event_time_race_round_length_invalid(
                nomination_event.race_round_length
            )
        self.__event_manager.raise_exception_if_owner_wrong(event_db, user_db.id)
        self.__nomination_event_manager.append(nomination_db, event_db, user_db, nomination_event)
        return {"message": self.__nominations_appended_message}

    def get_nomination_event_data(
            self,
            response: Response,
            token: str,
            event_id: int
    ):
        self.__token_manager.decode_token(token, response)
        event_db = self.__event_manager.get_by_id_or_raise_if_not_found(event_id)
        return self.__nomination_event_manager.get_nomination_event_data(event_db)

    def delete(self, response: Response, token: str, nomination_event: NominationEventSchema):
        decoded_token, event_db, nomination_db, nomination_event_db = \
            self.get_decoded_token_event_nomination_nomination_event(response, token, nomination_event)
        self.__event_manager.raise_exception_if_owner_wrong(event_db, decoded_token.user_id)
        self.__nomination_event_manager.delete(nomination_event_db)
        return {"message": self.__nomination_event_deleted_message}

    def close_registration(
            self,
            response: Response,
            token: str,
            nomination_event: NominationEventSchema
    ):
        decoded_token, event_db, nomination_db, nomination_event_db = \
            self.get_decoded_token_event_nomination_nomination_event(response, token, nomination_event)
        self.__event_manager.raise_exception_if_owner_wrong(event_db, decoded_token.user_id)
        self.__nomination_event_manager.close_registration(nomination_event_db)
        return {"message": self.__registration_closed_message}

    def open_registration(
            self,
            response: Response,
            token: str,
            nomination_event: NominationEventSchema
    ):
        decoded_token, event_db, nomination_db, nomination_event_db =\
            self.get_decoded_token_event_nomination_nomination_event(response, token, nomination_event)
        self.__event_manager.raise_exception_if_owner_wrong(event_db, decoded_token.user_id)
        self.__nomination_event_manager.raise_exception_if_tournament_started(nomination_event_db)
        self.__nomination_event_manager.open_registration(nomination_event_db)
        return {"message": self.__registration_opened_message}

    def get_decoded_token_event_nomination_nomination_event(
        self,
        response: Response,
        token: str,
        nomination_event: NominationEventSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        event_db = self.__event_manager.get_by_id_or_raise_if_not_found(nomination_event.event_id)
        nomination_db = self.__nomination_manager.get_by_name_and_user_id_or_raise_exception_if_not_found(
            decoded_token.user_id,
            nomination_event.nomination_name
        )
        nomination_event_db = self.__nomination_event_manager.get_nomination_event_or_raise_if_not_found(
            nomination_db,
            event_db,
            nomination_event.type
        )
        return decoded_token, event_db, nomination_db, nomination_event_db
