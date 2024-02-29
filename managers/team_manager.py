from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db import models
from db.crud.team import get_teams_by_owner_db, create_team_db, get_team_by_name_db, get_teams_db
from db.schemas.team import TeamSchema


class TeamManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__team_name_taken_error = "team name taken"
        self.__team_not_found_error = "team not found"
        self.__wrong_team_owner_error = "this team is not yours"
        self.__participant_in_another_team_error = "participant in another team"

    def get_teams(self, offset: int, limit: int) -> list[TeamSchema]:
        teams_db = get_teams_db(self.__db, offset, limit)
        teams = [TeamSchema.from_orm(team_db) for team_db in teams_db]
        return teams

    def get_teams_by_owner(self, offset: int, limit: int, owner_id: int) -> list[TeamSchema]:
        teams_db = get_teams_by_owner_db(self.__db, offset, limit, owner_id)
        teams = [TeamSchema.from_orm(team_db) for team_db in teams_db]
        return teams

    def create_team(self, team: TeamSchema, creator_id: int):
        self.raise_exception_if_team_name_taken(team.name)
        create_team_db(self.__db, team, creator_id)

    def get_team_by_name(self, name: str) -> TeamSchema | None:
        team_db = get_team_by_name_db(self.__db, name)
        if team_db:
            return TeamSchema.from_orm(team_db)

    def get_emails_of_team(self, team_db: models.Team):
        emails = set()
        for participant_db in team_db.participants:
            emails.add(participant_db.email)
        return emails

    def raise_exception_if_team_owner_wrong(self, team_name: str, user_id: int):
        team_db = get_team_by_name_db(self.__db, team_name)
        if team_db.creator_id != user_id:
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

    def raise_exception_if_team_not_found(self, team_name: str):
        team = self.get_team_by_name(team_name)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__team_not_found_error}
            )
