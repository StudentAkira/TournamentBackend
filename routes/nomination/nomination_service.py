from starlette.responses import Response

from db.schemas.nomination import NominationSchema
from managers.event import EventManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.token import TokenManager
from managers.user import UserManager


class NominationsService:

    def __init__(self, db):
        self.__db = db

        self.__nomination_manager = NominationManager(db)
        self.__token_manager = TokenManager(db)
        self.__user_manager = UserManager(db)
        self.__event_manager = EventManager(db)
        self.__nomination_event_manager = NominationEventManager(db)

        self.__nominations_created_message = "nominations created"
        self.__nomination_created_message = "nomination created"
        self.__nomination_updated_message = "nomination updated"

    def list(self, offset, limit) -> list[NominationSchema]:
        nominations = self.__nomination_manager.list(offset, limit)
        return nominations

    def create(self,  response: Response, token: str, nomination: NominationSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        self.__nomination_manager.raise_exception_if_name_taken(nomination.name)
        self.__nomination_manager.create(nomination)
        return {"message": self.__nomination_created_message}

    def create_many(self,  response: Response, token: str, nominations: list):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        self.__nomination_manager.create_many(nominations)
        return {"message": self.__nominations_created_message}

    def update(
            self,
            response: Response,
            token: str,
            old_nomination: NominationSchema,
            new_nomination: NominationSchema
    ):
        self.__token_manager.decode_token(token, response)
        self.__nomination_manager.raise_exception_if_name_taken(new_nomination.name)
        self.__nomination_manager.raise_exception_if_not_found(old_nomination.name)
        self.__nomination_manager.update(old_nomination, new_nomination)
        return {"message": self.__nomination_updated_message}

    def delete(
            self,
            response: Response,
            token: str,
            nomination_name: str
    ):
        self.__token_manager.decode_token(token, response)
        self.__nomination_manager.raise_exception_if_not_found(nomination_name)
        self.__nomination_manager.delete(nomination_name)
