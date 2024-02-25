from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db import models
from db.crud import create_team_db, get_team_by_name_db, get_my_teams_db
from db.schemas import Team


class TeamManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__team_created_message = "team created"

        self.__team_name_taken_error = "team name taken"

    def get_my_teams(self, offset: int, limit: int, owner_id: int):
        return get_my_teams_db(self.__db, offset, limit, owner_id)

    def create_team(self, team: Team, creator_id: int):
        self.raise_exception_if_team_name_taken(team.name)
        create_team_db(self.__db, team, creator_id)
        return {"message": self.__team_created_message}

    def get_team_by_name(self, name: str) -> models.Team | None:
        return get_team_by_name_db(self.__db, name)

    def raise_exception_if_team_name_taken(self, name: str):
        team = self.get_team_by_name(name)
        if team:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_name_taken_error}
            )
