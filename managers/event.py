from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.event.event import create_event_db, \
    get_events_by_owner_db, get_events_db, get_events_with_nominations_db, \
    get_events_with_nominations_by_owner_db, get_event_by_name_db, update_event_db, delete_event_db
from db.models.event import Event
from db.schemas.event.event import EventSchema
from db.schemas.event.event_create import EventCreateSchema
from db.schemas.event.event_update import EventUpdateSchema


class EventManager:

    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__event_name_taken_error = "event name taken"
        self.__event_does_not_exist_error = "event does not exist"
        self.__wrong_event_owner_error = "this event is not yours"
        self.__user_not_in_judge_command_error = "user not in judge command"

    def create(self, event: EventCreateSchema, owner_id: int):
        event_db = get_event_by_name_db(self.__db, event.name)
        if event_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__event_name_taken_error}
            )
        create_event_db(self.__db, event, owner_id)

    def list(self, offset: int, limit: int) -> list[EventSchema]:
        events_db = get_events_db(self.__db, offset, limit)
        events = [EventSchema.from_orm(event_db) for event_db in events_db]
        return events

    def list_by_owner(self, offset: int, limit: int, owner_id: int) -> list:
        events_db = get_events_by_owner_db(self.__db, offset, limit, owner_id)
        events = [EventSchema.from_orm(event_db) for event_db in events_db]
        return events

    def list_with_nominations(self, offset, limit):
        return get_events_with_nominations_db(self.__db, offset, limit)

    def list_with_nominations_by_owner(self, offset, limit, owner_id):
        return get_events_with_nominations_by_owner_db(self.__db, offset, limit, owner_id)

    def get_by_name_or_raise_if_not_found(self, name: str) -> type(Event):
        event_db = get_event_by_name_db(self.__db, name)
        if not event_db:
            raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail={"error": self.__event_does_not_exist_error}
            )
        return event_db

    def update(self, event_data: EventUpdateSchema):
        event_db = get_event_by_name_db(self.__db, event_data.new_name)
        if event_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__event_name_taken_error}
            )
        event_db = self.get_by_name_or_raise_if_not_found(event_data.old_name)
        update_event_db(self.__db, event_db, event_data)

    def delete(self, event_db: type(Event)):
        delete_event_db(self.__db, event_db)

    def raise_exception_if_owner_wrong(self, event_db: type(Event), user_id: int):
        if event_db.owner_id != user_id:#todo with judge command
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__wrong_event_owner_error}
            )
