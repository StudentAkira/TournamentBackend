from starlette.responses import Response

from db.schemas.participant import ParticipantSchema
from db.schemas.team import TeamSchema
from managers.team_manager import TeamManager
from managers.token_manager import TokenManager


class TeamsService:
    def __init__(self, db):
        self.__db = db
        self.__token_manager = TokenManager(db)
        self.__team_manager = TeamManager(db)

        self.__team_created_message = "team created"
        self.__team_appended_message = "team appended"

    def create_team(self, response, token: str, team: TeamSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__team_manager.create_team(team, decoded_token.user_id)
        return {"message": self.__team_created_message}

    def get_teams_by_owner(self, response, token, offset: int, limit: int):
        decoded = self.__token_manager.decode_token(token, response)
        return self.__team_manager.get_teams_by_owner(offset, limit, decoded.user_id)

    def append_participants_for_team(
            self,
            response: Response,
            token: str,
            teams: TeamSchema,
            participant: list[ParticipantSchema]
    ):
        pass
