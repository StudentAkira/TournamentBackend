from starlette.responses import Response

from db.schemas.event import EventSchema, EventCreateSchema
from db.schemas.user import UserRole
from managers.event_manager import EventManager
from managers.token_manager import TokenManager
from managers.user_manager import UserManager


class EventsService:

    def __init__(self, db):
        self.__db = db
        self.__token_manager = TokenManager(db)
        self.__user_manager = UserManager(db)
        self.__event_manager = EventManager(db)

        self.__event_created_message = "event created"

    def get_events(self, offset, limit) -> list[EventSchema]:
        events = self.__event_manager.get_events(offset, limit)
        return events

    def get_events_by_owner(self, response: Response, token: str, offset, limit) -> list[EventSchema]:
        decoded_token = self.__token_manager.decode_token(token, response)
        events = []
        if decoded_token.role == UserRole.specialist or decoded_token.role == UserRole.admin:
            events = self.get_events(offset, limit)
        if decoded_token.role == UserRole.judge:
            events = self.__event_manager.get_events_by_owner(offset, limit, decoded_token.user_id)
        return events

    def create_event(self, response: Response, token: str, event: EventCreateSchema) -> dict[str, str]:
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        self.__event_manager.create_event(event, decoded_token.user_id)
        return {"message": self.__event_created_message}


