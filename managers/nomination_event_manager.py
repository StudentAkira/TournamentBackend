from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.nomination_event import get_nomination_event_db
from db.schemas.team import TeamSchema


class NominationEventManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__nomination_event_does_not_exist_error = "nomination event does not exist"

    def get_nomination_event_teams(self, event_name: str, nomination_name: str) -> list[TeamSchema]:
        nomination_event_db = get_nomination_event_db(self.__db, event_name, nomination_name)
        return [TeamSchema.from_orm(team_db) for team_db in nomination_event_db.teams]

    def raise_exception_if_nomination_event_not_found(self, event_name: str, nomination_name: str):
        nomination_event = get_nomination_event_db(self.__db, event_name, nomination_name)
        if not nomination_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__nomination_event_does_not_exist_error}
            )
