from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db import models
from db.crud import get_event_by_name_db, create_event_db, append_event_nominations_db
from db.schemas import EventCreate, BaseNomination, Event


class EventManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__event_name_taken_error = "event name taken"
        self.__event_does_not_exist_error = "event does not exist"

        self.__event_created_message = "event created"
        self.__nominations_appended_message = "nominations appended"
        self.__wrong_event_owner_error = "this event is not yours"

    def create_event(self, event: EventCreate, owner_id: int):
        self.raise_exception_if_event_name_taken(event.name)
        create_event_db(self.__db, event, owner_id)
        return {"message": self.__event_created_message}

    def append_nominations(self, event: Event, nominations: list[BaseNomination]):
        append_event_nominations_db(self.__db, event, nominations)
        return {"message": self.__nominations_appended_message}

    def raise_exception_if_event_name_taken(self, name):
        event = get_event_by_name_db(self.__db, name)
        if event:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__event_name_taken_error}
            )

    def get_event_by_name(self, name: str):
        event = get_event_by_name_db(self.__db, name)
        return event

    def raise_exception_if_event_owner_wrong(self, event_name: str, user_id: str):
        event_db = self.get_event_by_name(event_name)
        if event_db.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__event_does_not_exist_error}
            )

    def raise_exception_if_event_dont_exist(self, name):
        event = self.get_event_by_name(name)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__event_does_not_exist_error}
            )
