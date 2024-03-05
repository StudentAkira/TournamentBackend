from pydantic import EmailStr
from starlette.responses import Response

from db.schemas.participant import ParticipantSchema
from db.schemas.team import TeamSchema
from db.schemas.token import TokenDecodedSchema
from db.schemas.user import UserRole
from managers.paticipant_manager import ParticipantManager
from managers.team_manager import TeamManager
from managers.token_manager import TokenManager


class ParticipantsService:

    def __init__(self, db):
        self.__db = db

        self.__token_manager = TokenManager(db)
        self.__participant_manager = ParticipantManager(db)
        self.__team_manager = TeamManager(db)

        self.__participant_created_message = "participant created"
        self.__participant_appended_to_team_message = "participant appended to team"

    def get_participants_by_owner(
            self,
            response: Response,
            token: str,
            offset: int,
            limit: int
    ) -> list[ParticipantSchema]:
        decoded_token = self.__token_manager.decode_token(token, response)
        return self.__participant_manager.get_participants_by_owner(offset, limit, decoded_token.user_id)

    def create_participant(self, response: Response, token: str, participant: ParticipantSchema) -> dict[str, str]:
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__participant_manager.create_participant(participant, decoded_token.user_id)
        return {"message": self.__participant_created_message}

    def append_participant_to_team(
            self,
            response: Response,
            token: str,
            participant_email: EmailStr,
            team_name: str,
    ) -> dict[str, str]:
        decoded_token = self.__token_manager.decode_token(token, response)
        self.check_entities_existence(participant_email, team_name)
        self.check_ownership_for_not_admin(decoded_token, participant_email, team_name)

        participant = self.__participant_manager.get_participant_by_email(participant_email)
        team = self.__team_manager.get_team_by_name(team_name)
        self.__participant_manager.raise_exception_if_participant_already_in_team(participant, team)
        self.__team_manager.check_if_team_default(team)
        self.__participant_manager.append_participant_to_team(participant, team)

        return {"message": self.__participant_appended_to_team_message}

    def check_entities_existence(self, participant_email: EmailStr, team_name: str):
        self.__participant_manager.raise_exception_if_participant_not_found(participant_email)
        self.__team_manager.raise_exception_if_team_not_found(team_name)

    def check_ownership_for_not_admin(self, decoded_token: TokenDecodedSchema, participant_email: str, team_name: str):
        if decoded_token.role != UserRole.admin:
            self.__team_manager.raise_exception_if_team_owner_wrong(team_name, decoded_token.user_id)
            self.__participant_manager.raise_exception_if_participant_owner_wrong(participant_email,
                                                                                  decoded_token.user_id)
