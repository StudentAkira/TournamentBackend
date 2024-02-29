from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db import models
from db.crud.team import get_teams_by_owner_db, create_team_db, get_team_by_name_db, get_teams_by_event_nomination_db, \
    get_teams_db, append_team_to_nomination_event_db
from db.schemas.team import TeamSchema


class TeamManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__team_name_taken_error = "team name taken"
        self.__team_not_found_error = "team not found"
        self.__wrong_team_owner_error = "this team is not yours"
        self.__participant_in_another_team_error = "participant in another team"
        self.__team_already_in_nomination_event_error = "team already in nomination event"

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
        team_db = self.get_db_team_by_name(name)
        if team_db:
            return TeamSchema.from_orm(team_db)

    def get_db_team_by_name(self, name) -> type(models.Team) | None:
        team_db = get_team_by_name_db(self.__db, name)
        return team_db

    def append_team_to_event_nomination(self, team_name: str, nomination_name: str, event_name: str):
        emails_of_all_participants_in_event_nomination = self.get_emails_of_all_participants_in_event_nomination(
            event_name,
            nomination_name
        )
        received_team_db = self.get_db_team_by_name(team_name)
        received_team_participants_emails = self.get_emails_of_team(received_team_db)

        self.raise_exception_if_participant_in_existing_team(
            emails_of_all_participants_in_event_nomination,
            received_team_participants_emails
        )
        append_team_to_nomination_event_db(self.__db, team_name, event_name, nomination_name)

    def get_emails_of_all_participants_in_event_nomination(self, event_name, nomination_name):
        teams_db = get_teams_by_event_nomination_db(self.__db, event_name, nomination_name)
        emails = set()
        for team_db in teams_db:
            emails.union(self.get_emails_of_team(team_db))
        return emails

    def get_emails_of_team(self, team_db: models.Team):
        emails = set()
        for participant_db in team_db.participants:
            emails.add(participant_db.email)
        return emails

    def get_teams_of_event_nomination(self, event_name: str, nomination_name: str) -> list[TeamSchema]:
        teams_db = get_teams_by_event_nomination_db(self.__db, event_name, nomination_name)
        teams = [TeamSchema.from_orm(team_db) for team_db in teams_db]
        return teams

    def raise_exception_if_team_owner_wrong(self, team_name: str, user_id: int):
        team_db = self.get_db_team_by_name(team_name)
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
                detail={"error": self.__team_name_taken_error}
            )

    def raise_exception_if_participant_in_existing_team(
            self,
            team_participants_emails: set,
            teams_participants_emails: set
    ):
        if len(teams_participants_emails.intersection(team_participants_emails)) != 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_in_another_team_error}
            )

    def raise_exception_if_team_already_in_nomination_event(self, team_name: str, nomination_name: str, event_name: str):
        teams_names = set(team.name for team in self.get_teams_of_event_nomination(nomination_name, event_name))
        if team_name in teams_names:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_already_in_nomination_event_error}
            )
