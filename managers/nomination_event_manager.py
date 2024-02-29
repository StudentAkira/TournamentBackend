from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.nomination_event import get_nomination_event_db
from db.crud.team import get_teams_by_event_nomination_db, get_team_by_name_db, append_team_to_nomination_event_db
from db.schemas.team import TeamSchema
from managers.team_manager import TeamManager


class NominationEventManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__team_manager = TeamManager(db)

        self.__nomination_event_does_not_exist_error = "nomination event does not exist"
        self.__team_already_in_nomination_event_error = "team already in nomination event"

    def get_nomination_event_teams(self, nomination_name: str, event_name: str) -> list[TeamSchema]:
        nomination_event_db = get_nomination_event_db(self.__db, nomination_name, event_name)
        return [TeamSchema.from_orm(team_db) for team_db in nomination_event_db.teams]

    def get_teams_of_event_nomination(self, nomination_name: str, event_name: str) -> list[TeamSchema]:
        teams_db = get_teams_by_event_nomination_db(self.__db, nomination_name, event_name)
        teams = [TeamSchema.from_orm(team_db) for team_db in teams_db]
        return teams

    def append_team_to_event_nomination(self, team_name: str, nomination_name: str, event_name: str):
        emails_of_all_participants_in_event_nomination = self.get_emails_of_all_participants_in_event_nomination(
            event_name,
            nomination_name
        )
        received_team_db = get_team_by_name_db(self.__db, team_name)
        received_team_participants_emails = self.__team_manager.get_emails_of_team(received_team_db)

        self.__team_manager.raise_exception_if_participant_in_existing_team(
            emails_of_all_participants_in_event_nomination,
            received_team_participants_emails
        )
        append_team_to_nomination_event_db(self.__db, team_name, nomination_name, event_name)

    def get_emails_of_all_participants_in_event_nomination(self, event_name, nomination_name):
        teams_db = get_teams_by_event_nomination_db(self.__db, nomination_name, event_name)
        emails = set()
        for team_db in teams_db:
            emails.union(self.__team_manager.get_emails_of_team(team_db))
        return emails

    def raise_exception_if_nomination_event_not_found(self, nomination_name: str, event_name: str):
        nomination_event = get_nomination_event_db(self.__db, nomination_name,  event_name)
        if not nomination_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__nomination_event_does_not_exist_error}
            )

    def raise_exception_if_team_already_in_nomination_event(
            self,
            team_name: str,
            nomination_name: str,
            event_name: str
    ):
        teams_names = set(team.name for team in self.get_teams_of_event_nomination(nomination_name, event_name))
        print("teams names :: ", teams_names)
        if team_name in teams_names:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_already_in_nomination_event_error}
            )
