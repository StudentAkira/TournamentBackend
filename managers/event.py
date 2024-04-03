from typing import cast

from fastapi import HTTPException
from sqlalchemy import exists
from sqlalchemy.orm import Session
from starlette import status

from db.crud.event import create_event_db, get_event_by_name_db, get_events_by_owner_db, \
    get_events_db, update_event_db, get_events_with_nominations_db, get_events_with_nominations_by_owner_db, \
    delete_event_db
from db.crud.nomination_event import get_judge_command_ids_db
from db.models.event import Event
from db.schemas.event import EventCreateSchema, EventSchema, EventUpdateSchema, EventDeleteSchema


class EventManager:

    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__event_name_taken_error = "event name taken"
        self.__event_does_not_exist_error = "event does not exist"
        self.__wrong_event_owner_error = "this event is not yours"
        self.__user_not_in_judge_command_error = "user not in judge command"

    def create(self, event: EventCreateSchema, owner_id: int):
        self.raise_exception_if_name_taken(event.name)
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

    def read_by_name(self, name: str) -> EventSchema | None:
        event_db = get_event_by_name_db(self.__db, name)
        if event_db:
            return EventSchema.from_orm(event_db)

    def update(self, event_data: EventUpdateSchema):
        self.raise_exception_if_name_taken(event_data.new_name)
        update_event_db(self.__db, event_data)

    def delete(self, event_data: EventDeleteSchema):
        delete_event_db(self.__db, event_data)

    def raise_exception_if_name_taken(self, event_name: str):
        entity_exists = self.__db.query(
            exists().where(cast("ColumnElement[bool]", Event.name == event_name))).scalar()
        if entity_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__event_name_taken_error}
            )

    def raise_exception_if_owner_wrong(self, event_name: str, user_id: int):
        event_db = get_event_by_name_db(self.__db, event_name)
        if event_db.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__wrong_event_owner_error}
            )

    def raise_exception_if_user_not_in_judge_command(
            self,
            nomination_name: str,
            event_name: str,
            nomination_event_type: str,
            user_id: int
    ):
        judge_command_ids = get_judge_command_ids_db(self.__db, nomination_name, event_name, nomination_event_type)
        if user_id not in judge_command_ids:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__user_not_in_judge_command_error}
            )

    def raise_exception_if_not_found(self, event_name: str):
        entity_exists = self.__db.query(
            exists().where(
                cast("ColumnElement[bool]", Event.name == event_name)
            )
        ).scalar()
        if not entity_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__event_does_not_exist_error}
            )
