from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event.nomination_event import NominationEventSchema
from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema
from managers.event import EventManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.token import TokenManager
from managers.user import UserManager


class Retriever:
    def __init__(self, db: Session):
        self.__db = db

        self.__nomination_event_manager = NominationEventManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__event_manager = EventManager(db)
        self.__user_manager = UserManager(db)
        self.__token_manager = TokenManager(db)

    def get_decoded_token_user_nomination_event_nomination_event(
            self,
            response: Response,
            token: str,
            nomination_event: NominationEventSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        user_db = self.__user_manager.get_user_by_id_or_raise_if_not_found(decoded_token.user_id)
        event_db = self.__event_manager.get_by_name_or_raise_if_not_found(
            nomination_event.event_name
        )
        nomination_db = self.__nomination_manager.get_by_name_and_user_id_or_raise_exception_if_not_found(
            nomination_event.nomination_name
        )
        nomination_event_db = self.__nomination_event_manager.get_nomination_event_or_raise_if_not_found(
            nomination_db,
            event_db,
            nomination_event.type
        )
        return decoded_token, user_db, event_db, nomination_db, nomination_event_db

    def get_decoded_token_user_nomination_event_nomination_event_check_judge_in_command(
            self,
            response: Response,
            token: str,
            nomination_event: OlympycNominationEventSchema
    ):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.get_decoded_token_user_nomination_event_nomination_event(
                response,
                token,
                nomination_event.to_nomination_event_schema()
            )
        self.__nomination_event_manager.raise_exception_if_user_not_in_judge_command(
            nomination_event_db,
            user_db
        )
        return decoded_token, user_db, event_db, nomination_db, nomination_event_db
