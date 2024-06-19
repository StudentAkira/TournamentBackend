from starlette.responses import Response

from db.crud.nomination.nomination import get_nomination_by_name_and_user_id_db
from db.schemas.nomination.nomination import NominationSchema
from db.schemas.nomination.nomination_create import NominationCreateSchema
from db.schemas.nomination.nomination_get import NominationGetSchema
from db.schemas.nomination.nomination_update import NominationUpdateSchema
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

    def list(self, response: Response, token: str, offset: int, limit: int) -> list[NominationGetSchema]:
        decoded_token = self.__token_manager.decode_token(token, response)
        nominations = self.__nomination_manager.list(decoded_token.user_id, offset, limit)
        return nominations

    def create(self,  response: Response, token: str, nomination_data: NominationCreateSchema) -> dict[str, str]:
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        nomination_db = get_nomination_by_name_and_user_id_db(self.__db, decoded_token.user_id, nomination_data.name)
        self.__nomination_manager.raise_exception_if_name_taken(nomination_db)
        self.__nomination_manager.create(decoded_token.user_id, nomination_data)
        return {"message": self.__nomination_created_message}

    def update(
            self,
            response: Response,
            token: str,
            nomination_data: NominationUpdateSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        nomination_db = self.__nomination_manager.get_by_id_and_user_id(decoded_token.user_id, nomination_data.id)
        self.__nomination_manager.raise_exception_if_not_found(nomination_db)

        new_nomination_db = get_nomination_by_name_and_user_id_db(
            self.__db,
            decoded_token.user_id,
            nomination_data.new_name
        )
        self.__nomination_manager.raise_exception_if_name_taken(new_nomination_db)

        self.__nomination_manager.update(nomination_db, nomination_data)
        return {"message": self.__nomination_updated_message}

    def get_nominations_related_to_event(self, event_id: int, offset: int, limit: int) -> list:
        event_db = self.__event_manager.get_by_id(event_id)
        self.__event_manager.raise_exception_if_event_not_found(event_db)
        return [NominationSchema.from_orm(nomination_db) for nomination_db in
                self.__nomination_manager.get_event_related_nominations(event_db, offset, limit)]

    def get_nominations_not_related_to_event(self, event_id: int, offset: int, limit: int):
        event_db = self.__event_manager.get_by_id(event_id)
        self.__event_manager.raise_exception_if_event_not_found(event_db)
        return [NominationSchema.from_orm(nomination_db) for nomination_db in
                self.__nomination_manager.get_event_not_related_nominations(event_db, offset, limit)]

    def get_nominations_related_to_event_starts_with(self, event_id: int, title: str, offset: int, limit: int):
        event_db = self.__event_manager.get_by_id(event_id)
        self.__event_manager.raise_exception_if_event_not_found(event_db)
        return [NominationSchema.from_orm(nomination_db) for nomination_db in
                self.__nomination_manager.get_event_related_nominations_starts_with(event_db, title, offset, limit)]

    def get_nominations_not_related_to_event_starts_with(self, event_id: int, title: str, offset: int, limit: int):
        event_db = self.__event_manager.get_by_id(event_id)
        self.__event_manager.raise_exception_if_event_not_found(event_db)
        return [NominationSchema.from_orm(nomination_db) for nomination_db in
                self.__nomination_manager.get_event_not_related_nominations_starts_with(event_db, title, offset, limit)]
