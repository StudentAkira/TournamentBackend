from email.utils import parseaddr

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from db.crud.team.team import get_teams_db, get_teams_by_owner_db, create_team_db, update_team_db, get_team_by_name_db
from db.models.team import Team
from db.schemas.team.team import TeamSchema
from db.schemas.team.team_update import TeamUpdateSchema
from db.schemas.team_participant.team_participant import TeamParticipantsSchema
from managers.participant import ParticipantManager


class TeamManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db
        self.__participant_manager = ParticipantManager(db)

        self.__team_name_taken_error = "team name taken"
        self.__team_not_found_error = "team not found"
        self.__wrong_team_owner_error = "this team is not yours"
        self.__cant_append_participant_to_default_team_error = "you cant not append participant to default team"
        self.__cant_create_team_marked_as_default_error = "you cant not name team as default"
        self.__team_contains_email_address_error = "team cannot contain email address"
        self.__default_team_error = "default team is unchangeable"

    def list(self, offset: int, limit: int) -> list[TeamParticipantsSchema]:
        teams_db = get_teams_db(self.__db, offset, limit)
        teams = [TeamParticipantsSchema.from_orm(team_db) for team_db in teams_db]
        return teams

    def list_by_owner(self, offset: int, limit: int, owner_id: int) -> list:
        teams_db = get_teams_by_owner_db(self.__db, offset, limit, owner_id)
        teams = [TeamParticipantsSchema.from_orm(team_db) for team_db in teams_db]
        return teams

    def create(self, team: TeamSchema, creator_id: int):
        team_db = get_team_by_name_db(self.__db, team.name)
        self.raise_exception_if_name_taken(team_db)
        self.raise_exception_if_name_invalid(team)
        create_team_db(self.__db, team, creator_id)

    def update(self, team_db: type(Team), team_data: TeamUpdateSchema):
        update_team_db(self.__db, team_db, team_data)

    def check_entities_existence(self, team: TeamSchema, participant_emails: set[EmailStr]):
        self.raise_exception_if_name_taken(team.name)
        for participant_email in participant_emails:
            participant_db = self.__participant_manager.get_by_email_or_raise_if_not_found(participant_email)

    def get_by_name_or_raise_if_not_found(self, name: str) -> type(Team):
        team_db = get_team_by_name_db(self.__db, name)
        if not team_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__team_not_found_error}
            )
        return team_db

    def get_emails_of_team(self, team_db: Team):
        emails = set()
        for participant_db in team_db.participants:
            emails.add(participant_db.email)
        return emails

    def get_team_name_from_team_name_or_participant_email(self, team_name_or_participant_email):
        team_db = get_team_by_name_db(self.__db, team_name_or_participant_email)
        if team_db:
            return team_db.name
        participant = self.__participant_manager.read_by_email(team_name_or_participant_email)
        if participant:
            return f"default_team_{participant.email}"

    def raise_exception_if_owner_wrong(self, team_db: type(Team), user_id: int):
        if team_db.creator_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__wrong_team_owner_error}
            )

    def raise_exception_if_name_taken(self, team_db: type(Team)):
        if team_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_name_taken_error}
            )

    def raise_exception_if_name_invalid(self, team: TeamSchema):
        if '@' in parseaddr(team.name)[1]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_contains_email_address_error}
            )
        if "default_team" in team.name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__cant_create_team_marked_as_default_error}
            )

    def raise_exception_if_team_default(self, name: str):
        if "default_team" in name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__default_team_error}
            )
