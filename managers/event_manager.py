from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud import get_event_by_name_db, create_event_db
from db.schemas import EventCreate


class EventManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__event_name_taken_error = "event name taken"

        self.__event_created_message = "event created"

    def create_event(self, event: EventCreate, owner_id: int):
        self.raise_exception_if_event_name_taken(event.name)
        create_event_db(self.__db, event, owner_id)
        return {"message": self.__event_created_message}

    def raise_exception_if_event_name_taken(self, name):
        event = get_event_by_name_db(self.__db, name)
        if event:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__event_name_taken_error}
            )
