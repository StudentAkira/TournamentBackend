from starlette.responses import Response

from db.schemas.event import EventSchema
from db.schemas.nomination import NominationSchema
from managers.event import EventManager
from managers.nomination import NominationManager
from managers.token import TokenManager
from managers.user import UserManager


class NominationsService:

    def __init__(self, db):
        self.__db = db

        self.__nomination_manager = NominationManager(db)
        self.__token_manager = TokenManager(db)
        self.__user_manager = UserManager(db)
        self.__event_manager = EventManager(db)

        self.__nominations_created_message = "nomination created"
        self.__nominations_appended_message = "nomination appended"
        self.__nomination_updated_message = "nomination updated"

    def get_nominations(self, offset, limit) -> list[NominationSchema]:
        nominations = self.__nomination_manager.get_nominations(offset, limit)
        return nominations

    def create_nominations(self,  response: Response, token: str, nominations: list[NominationSchema]):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        self.__nomination_manager.create_nominations(nominations)
        return {"message": self.__nominations_created_message}

    def append_nominations_for_event(
            self,
            response: Response,
            token: str,
            event: EventSchema,
            nominations: list[NominationSchema]
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        self.__event_manager.raise_exception_if_event_not_found(event.name)
        self.__event_manager.append_nominations(event, nominations)
        return {"message": self.__nominations_appended_message}

    def update_nomination(
            self,
            response: Response,
            token: str,
            old_nomination: NominationSchema,
            new_nomination: NominationSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__nomination_manager.raise_exception_if_nomination_name_taken(new_nomination.name)
        self.__nomination_manager.update_nomination(old_nomination, new_nomination)
        return {"message": self.__nomination_updated_message}

    def delete_nomination(
            self,
            response: Response,
            token: str,
            nomination_name: str
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__nomination_manager.raise_exception_if_nomination_not_found(nomination_name)
        self.__nomination_manager.detele_nomination()