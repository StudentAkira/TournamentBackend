from starlette.responses import Response

from db.crud.team.team import get_team_by_name_db
from db.schemas.team.team_create import TeamCreateSchema
from db.schemas.team.team_update import TeamUpdateSchema
from db.schemas.team_participant.team_participant import TeamParticipantsSchema
from db.schemas.user.user_role import UserRole
from managers.event import EventManager
from managers.team import TeamManager
from managers.token import TokenManager
from managers.user import UserManager
from utils.validation_util import Validator


class TeamsService:
    def __init__(self, db):
        self.__db = db
        self.__token_manager = TokenManager(db)
        self.__team_manager = TeamManager(db)
        self.__event_manager = EventManager(db)
        self.__user_manager = UserManager(db)

        self.__validator = Validator(db)

        self.__team_created_message = "team created"
        self.__team_appended_message = "team appended"
        self.__software_and_equipment_set_message = "software & equipment was set"
        self.__team_updated_message = "team updated"

    def create_team(self, response, token: str, team: TeamCreateSchema) -> dict[str, str]:
        decoded_token = self.__token_manager.decode_token(token, response)
        user_db = self.__user_manager.get_user_by_id_or_raise_if_not_found(decoded_token.user_id)

        self.__team_manager.create(
            team,
            user_db
        )
        return {"message": self.__team_created_message}

    def list_by_owner(self, response: Response, token: str, offset: int, limit: int) -> list[TeamParticipantsSchema]:
        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role == UserRole.admin:
            return self.__team_manager.list(offset, limit)
        return self.__team_manager.list_by_owner(offset, limit, decoded_token.user_id)

    def update(self, response: Response, token: str, team_data: TeamUpdateSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__team_manager.raise_exception_if_name_invalid(team_data.new_name)

        team_db = self.__team_manager.get_by_id_or_raise_if_not_found(team_data.id)
        self.__team_manager.raise_exception_if_owner_wrong(team_db, decoded_token.user_id)
        self.__team_manager.raise_exception_if_team_default(team_db.name)

        existing_team_db = get_team_by_name_db(self.__db, team_data.new_name)
        self.__team_manager.raise_exception_if_name_taken(existing_team_db)
        self.__team_manager.update(team_db, team_data)
        return {"message": self.__team_updated_message}
