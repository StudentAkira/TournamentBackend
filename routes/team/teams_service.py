from starlette.responses import Response

from db.crud.team.team import get_team_by_name_db
from db.schemas.team.team import TeamSchema
from db.schemas.team.team_update import TeamUpdateSchema
from db.schemas.user.user_role import UserRole
from managers.event import EventManager
from managers.team import TeamManager
from managers.token import TokenManager
from utils.validation_util import Validator


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
            decoded_token.user_id
        )
        return {"message": self.__team_created_message}

    def list_by_owner(self, response: Response, token: str, offset: int, limit: int):
        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role == UserRole.admin:
            return self.__team_manager.list(offset, limit)
        return self.__team_manager.list_by_owner(offset, limit, decoded_token.user_id)

    def update(self, response: Response, token: str, team_data: TeamUpdateSchema):
        decoded_token = self.__token_manager.decode_token(token, response)

        team_db = self.__team_manager.get_by_name_or_raise_if_not_found(team_data.old_name)
        existing_team_db = get_team_by_name_db(self.__db, team_data.new_name)
        self.__team_manager.raise_exception_if_name_invalid(TeamSchema(name=team_data.new_name))
        self.__team_manager.raise_exception_if_name_taken(existing_team_db)
        self.__team_manager.raise_exception_if_owner_wrong(team_db, decoded_token.user_id)
        self.__team_manager.update(team_db, team_data)
        return {"message": self.__team_updated_message}
