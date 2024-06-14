from starlette.responses import Response

from db.crud.nomination.nomination import get_nomination_by_name_db
from db.schemas.nomination.nomination import NominationSchema
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
        nomination_db = get_nomination_by_name_db(self.__db, nomination.name)
        self.__nomination_manager.raise_exception_if_name_taken(nomination_db)
        self.__nomination_manager.create(nomination)
        return {"message": self.__nomination_created_message}

    def update(
            self,
            response: Response,
            token: str,
            old_nomination: NominationSchema,
            new_nomination: NominationSchema
    ):
        self.__token_manager.decode_token(token, response)
        nomination_db = self.__nomination_manager.get_by_name_or_raise_exception_if_not_found(old_nomination.name)
        new_nomination_db = get_nomination_by_name_db(self.__db, new_nomination.name)
        self.__nomination_manager.raise_exception_if_name_taken(new_nomination_db)
        self.__nomination_manager.update(nomination_db, new_nomination)
        return {"message": self.__nomination_updated_message}

    def get_nominations_related_to_event(self, event_id: int, offset: int, limit: int):
        event_db = self.__event_manager.get_by_id(event_id)
        self.__event_manager.raise_exception_if_event_not_found(event_db)
        return [NominationSchema.from_orm(nomination_db) for nomination_db in
                self.__nomination_manager.get_event_related_nominations(event_db, offset, limit)]

    def get_nominations_not_related_to_event(self, event_id: int, offset: int, limit: int):
        event_db = self.__event_manager.get_by_id(event_id)
        self.__event_manager.raise_exception_if_event_not_found(event_db)
        return [NominationSchema.from_orm(nomination_db) for nomination_db in
                self.__nomination_manager.get_event_non_related_nominations(event_db, offset, limit)]