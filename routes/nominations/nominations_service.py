from starlette.responses import Response

from db.schemas.event import EventSchema
from db.schemas.nomination import NominationSchema
from managers.event_manager import EventManager
from managers.nomination_manager import NominationManager
from managers.token_manager import TokenManager
from managers.user_manager import UserManager


class NominationsService:

    def __init__(self, db):
        self.__db = db

        self.__nomination_manager = NominationManager(db)
        self.__token_manager = TokenManager(db)
        self.__user_manager = UserManager(db)
        self.__event_manager = EventManager(db)

        self.__nominations_created_message = "nominations created"
        self.__nominations_appended_message = "nominations appended"

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
        self.__event_manager.raise_exception_if_event_not_found(event)
        self.__event_manager.append_nominations(event, nominations)
        return {"message": self.__nominations_appended_message}
