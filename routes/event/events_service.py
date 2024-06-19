from starlette.responses import Response

from db.schemas.event.event import EventSchema
from db.schemas.event.event_by_id import EventByIdSchema
from db.schemas.event.event_create import EventCreateSchema
from db.schemas.event.event_delete import EventDeleteSchema
from db.schemas.event.event_update import EventUpdateSchema
from db.schemas.user.user_role import UserRole
from managers.event import EventManager
from managers.token import TokenManager
from managers.user import UserManager


class EventsService:

    def __init__(self, db):
        self.__db = db
        self.__token_manager = TokenManager(db)
        self.__user_manager = UserManager(db)
        self.__event_manager = EventManager(db)

        self.__event_created_message = "event created"
        self.__event_updated_message = "event updated"
        self.__event_deleted_message = "event deleted"

    def list(
            self,
            offset,
            limit
    ) -> list[EventSchema]:
        events = self.__event_manager.list(offset, limit)
        return events

    def list_by_owner(self, response: Response, token: str, offset, limit: int) -> list:
        decoded_token = self.__token_manager.decode_token(token, response)
        events = []
        if decoded_token.role == UserRole.specialist or decoded_token.role == UserRole.admin:
            events = self.list(offset, limit)
        if decoded_token.role == UserRole.judge:
            events = self.__event_manager.list_by_owner(offset, limit, decoded_token.user_id)
        return events

    def list_with_nominations(self, response: Response, token: str, offset: int, limit: int):
        decoded_token = self.__token_manager.decode_token(token, response)
        events = []
        if decoded_token.role == UserRole.specialist or decoded_token.role == UserRole.admin:
            events = self.__event_manager.list_with_nominations(offset, limit)
        if decoded_token.role == UserRole.judge:
            events = self.__event_manager.list_with_nominations_by_owner(offset, limit, decoded_token.user_id)
        return events

    def create(
            self,
            response: Response,
            token: str,
            event: EventCreateSchema
    ) -> dict[str, str]:
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        self.__event_manager.create(event, decoded_token.user_id)
        return {"message": self.__event_created_message}

    def update(
            self,
            response: Response,
            token: str,
            event_data: EventUpdateSchema,
    ) -> dict[str, str]:
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        self.__event_manager.update(event_data)
        return {"message": self.__event_updated_message}

    def delete(
            self,
            response: Response,
            token: str,
            event_data: EventDeleteSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        event_db = self.__event_manager.get_by_name_or_raise_if_not_found(event_data.name)
        self.__event_manager.raise_exception_if_owner_wrong(event_db, decoded_token.user_id)
        self.__event_manager.delete(event_db)
        return {"message": self.__event_deleted_message}

    def get_by_id(self, response: Response, token: str, event_id: int) -> EventByIdSchema:
        decoded_token = self.__token_manager.decode_token(token, response)
        data = self.__event_manager.get_by_id_or_raise_exception_if_not_found(decoded_token, event_id)
        return data
