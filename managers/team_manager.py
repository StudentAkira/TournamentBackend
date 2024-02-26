from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db import models
from db.crud import create_team_db, get_team_by_name_db, get_my_teams_db, get_teams_of_event_nomination_db
from db.schemas import Team


class TeamManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__team_created_message = "team created"

        self.__team_name_taken_error = "team name taken"
        self.__team_not_found_error = "team not found"
        self.__wrong_team_owner_error = "this team is not yours"

    def get_my_teams(self, offset: int, limit: int, owner_id: int):
        return get_my_teams_db(self.__db, offset, limit, owner_id)

    def create_team(self, team: Team, creator_id: int):
        self.raise_exception_if_team_name_taken(team.name)
        create_team_db(self.__db, team, creator_id)
        return {"message": self.__team_created_message}

    def get_team_by_name(self, name: str) -> models.Team | None:
        return get_team_by_name_db(self.__db, name)

    def append_team_to_event_nomination(self, team_name: str, event_name: str, nomination_name: str):
        #check if player in another team
        teams = self.get_teams_of_event_nomination(event_name, nomination_name)

    def get_teams_of_event_nomination(self, event_name: str, nomination_name: str):
        return get_teams_of_event_nomination_db(self.__db, event_name, nomination_name)

    def raise_exception_if_team_owner_wrong(self, team_name: str, user_id: str):
        team_db = self.get_team_by_name(team_name)
        if team_db.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__wrong_team_owner_error}
            )

    def raise_exception_if_team_name_taken(self, name: str):
        team = self.get_team_by_name(name)
        if team:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_name_taken_error}
            )

    def raise_exception_if_team_dont_exist(self, name: str):
        team = self.get_team_by_name(name)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__team_name_taken_error}
            )
