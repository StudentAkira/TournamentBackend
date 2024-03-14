from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.event import get_event_by_name_db
from db.crud.nomination_event import get_nomination_events_full_info_db, \
    get_nomination_events_all_names_by_owner_db, \
    get_nomination_events_full_info_by_owner_db, \
    get_nomination_events_all_names_db, append_event_nominations_db
from db.schemas.event import EventSchema
from db.schemas.nomination_event import NominationEventSchema
from managers.event import EventManager
from managers.nomination import NominationManager
from managers.team import TeamManager


class NominationEventManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__team_manager = TeamManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__event_manager = EventManager(db)

        self.__nomination_event_does_not_exist_error = "nomination event does not exist"
        self.__tournament_already_started_error = "tournament already started"

    def list(self, offset: int, limit: int) -> list[NominationEventSchema]:
        nominations_events = get_nomination_events_all_names_db(self.__db, offset, limit)
        return nominations_events

    def list_by_owner(
            self, offset: int, limit: int, owner_id: int) -> list:
        nominations_events = get_nomination_events_all_names_by_owner_db(self.__db, offset, limit, owner_id)
        return nominations_events

    def list_full_info(self, offset: int, limit: int) -> list:
        nominations_events = get_nomination_events_full_info_db(self.__db, offset, limit)
        return nominations_events

    def list_full_info_by_owner(
            self, offset: int, limit: int, owner_id: int) -> list:
        nominations_events = get_nomination_events_full_info_by_owner_db(self.__db, offset, limit, owner_id)
        return nominations_events

    def append_many(self, event: EventSchema, nominations: list):
        append_event_nominations_db(self.__db, event, nominations)

    def raise_exception_if_not_found(self, nomination_name: str, event_name: str):

        self.__nomination_manager.raise_exception_if_not_found(nomination_name)
        self.__event_manager.raise_exception_if_not_found(event_name)

        event_nominations = set(nomination.name
                                for nomination in get_event_by_name_db(self.__db, event_name).nominations)

        if nomination_name not in event_nominations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__nomination_event_does_not_exist_error}
            )