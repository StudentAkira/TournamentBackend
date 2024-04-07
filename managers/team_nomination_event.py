from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.team.team import get_team_by_name_db
from db.crud.team_nomination_event.team_nomination_event import get_nomination_event_teams_db
from db.schemas.team.team import TeamSchema


class TeamNominationEventManager:
    __db: Session

    def __init__(self, db):
        self.__db = db

        self.__team_not_in_nomination_event_error = "team not in event nomination error"

    def list_teams_of_nomination_event(
            self,
            nomination_name: str,
            event_name: str,
            nomination_event_type: str
        ) -> list[TeamSchema]:
        teams_db = get_nomination_event_teams_db(self.__db, nomination_name, event_name, nomination_event_type)
        teams = [TeamSchema.from_orm(team_db) for team_db in teams_db]
        return teams

    def raise_exception_if_team_not_in_event_nomination(self, team_name: str, nomination_name: str, event_name: str):
        team_db = get_team_by_name_db(self.__db, team_name)
        teams_db = get_nomination_event_teams_db(self.__db, nomination_name, event_name)#todo

        if team_db not in teams_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_not_in_nomination_event_error}
            )
