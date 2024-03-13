from pydantic import EmailStr
from starlette.responses import Response

from db.schemas.team import TeamSchema
from db.schemas.user import UserRole
from managers.event import EventManager
from managers.team import TeamManager
from managers.token import TokenManager
from validators.validator import Validator


class TeamsService:
    def __init__(self, db):
        self.__db = db
        self.__token_manager = TokenManager(db)
        self.__team_manager = TeamManager(db)
        self.__event_manager = EventManager(db)

        self.__validator = Validator(db)

        self.__team_created_message = "team created"
        self.__team_appended_message = "team appended"
        self.__software_and_equipment_set_message = "software & equipment was set"

    def create_team(self, response, token: str, team: TeamSchema, participants_emails: list[EmailStr]):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__team_manager.create_team(
            team,
            set(participants_emails),
            decoded_token.user_id)
        return {"message": self.__team_created_message}

    def get_teams_by_owner(self, response, token, offset: int, limit: int):
        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role == UserRole.admin:
            return self.__team_manager.get_teams(offset, limit)
        return self.__team_manager.get_teams_by_owner(offset, limit, decoded_token.user_id)

    def set_team_software_and_equipment_in_event_nomination(
            self,
            response: Response,
            token: str,
            team_name_or_participant_email: str,
            nomination_name: str,
            event_name: str,
            software: str,
            equipment: str
    ):
        decoded_token = self.__token_manager.decode_token(token, response)

        team_name = self.__team_manager.get_team_name_from_team_name_or_participant_email(
            team_name_or_participant_email
        )

        self.__validator.check_team_event_nomination__nomination_event__existence(
            team_name,
            nomination_name,
            event_name
        )
        self.__validator.check_if_team_not_in_event_nomination(
            team_name,
            nomination_name,
            event_name
        )

        self.__team_manager.raise_exception_if_team_owner_wrong(team_name, decoded_token.user_id)
        self.__event_manager.raise_exception_if_event_owner_wrong(event_name, decoded_token.user_id)
        self.__team_manager.set_team_software_and_equipment_in_event_nomination(
            team_name,
            nomination_name,
            event_name,
            software,
            equipment
        )
        return {"message": self.__software_and_equipment_set_message}
