from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.team_nomination_event.team_nomination_event import get_nomination_event_teams_db
from db.models.nomination_event import NominationEvent
from db.models.team import Team
from db.schemas.team.team_get import TeamGetSchema


class TeamNominationEventManager:
    __db: Session

    def __init__(self, db):
        self.__db = db

        self.__team_not_in_nomination_event_error = "team not in event nomination error"

    def list_teams_of_nomination_event(
            self,
            nomination_event_db: type(NominationEvent)
    ) -> list[TeamGetSchema]:
        teams_db = get_nomination_event_teams_db(self.__db, nomination_event_db)
        teams = [TeamGetSchema.from_orm(team_db) for team_db in teams_db]
        return teams

    def raise_exception_if_team_not_in_event_nomination(
            self,
            team_db: type(Team),
            nomination_event_db: type(NominationEvent)
    ):
        teams_db = get_nomination_event_teams_db(self.__db, nomination_event_db)

        if team_db not in teams_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_not_in_nomination_event_error}
            )
