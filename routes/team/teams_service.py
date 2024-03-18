from pydantic import EmailStr
from starlette.responses import Response

from db.schemas.team import TeamSchema, TeamUpdateSchema
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
        self.__team_updated_message = "team updated"

    def create_team(self, response, token: str, team: TeamSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__team_manager.create(
            team,
            decoded_token.user_id)
        return {"message": self.__team_created_message}

    def list_by_owner(self, response: Response, token: str, offset: int, limit: int):
        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role == UserRole.admin:
            return self.__team_manager.list(offset, limit)
        return self.__team_manager.list_by_owner(offset, limit, decoded_token.user_id)

    def update(self, response: Response, token: str, team_data: TeamUpdateSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__team_manager.raise_exception_if_not_found(team_data.old_name)
        self.__team_manager.raise_exception_if_name_taken(team_data.new_name)
        self.__team_manager.raise_exception_if_owner_wrong(team_data.old_name, decoded_token.user_id)
        self.__team_manager.update(team_data)
        return {"message": self.__team_updated_message}
