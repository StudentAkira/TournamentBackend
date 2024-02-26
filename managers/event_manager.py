from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db import models
from db.crud.event import create_event_db, get_event_by_name_db, get_events_by_owner_db, append_event_nominations_db, \
    get_events_db
from db.schemas.event import EventCreateSchema, EventSchema
from db.schemas.nomination import NominationSchema


class EventManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__event_name_taken_error = "event name taken"
        self.__event_does_not_exist_error = "event does not exist"
        self.__wrong_event_owner_error = "this event is not yours"

    def create_event(self, event: EventCreateSchema, owner_id: int):
        self.raise_exception_if_event_name_taken(event.name)
        create_event_db(self.__db, event, owner_id)

    def get_events(self, offset: int, limit: int) -> list[EventSchema]:
        events_db = get_events_db(self.__db, offset, limit)
        events = [EventSchema.from_orm(event_db) for event_db in events_db]
        return events

    def get_event_by_name(self, name: str) -> EventSchema | None:
        event_db = get_event_by_name_db(self.__db, name)
        if event_db:
            return EventSchema.from_orm(event_db)

    def get_events_by_owner(self, offset: int, limit: int, owner_id: int) -> list[EventSchema]:
        events_db = get_events_by_owner_db(self.__db, offset, limit, owner_id)
        events = [EventSchema.from_orm(event_db) for event_db in events_db]
        return events

    def append_nominations(self, event: EventSchema, nominations: list[NominationSchema]):
        append_event_nominations_db(self.__db, event, nominations)

    def raise_exception_if_event_name_taken(self, name):
        event_db = self.get_event_by_name(name)
        if event_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__event_name_taken_error}
            )

    def raise_exception_if_event_owner_wrong(self, event_name: str, user_id: int):
        event_db = self.get_event_by_name(event_name)
        if event_db.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__event_does_not_exist_error}
            )

    def raise_exception_if_event_dont_exist(self, event):
        event = self.get_event_by_name(event.name)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__event_does_not_exist_error}
            )
