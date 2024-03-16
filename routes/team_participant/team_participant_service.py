from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.token import TokenDecodedSchema
from db.schemas.user import UserRole
from managers.participant import ParticipantManager
from managers.team import TeamManager
from managers.team_participant import TeamParticipantManager
from managers.token import TokenManager
from validators.validator import Validator


class TeamParticipantService:
    __db: Session

    def __init__(self, db):
        self.__db = db

        self.__token_manager = TokenManager(db)
        self.__participant_manager = ParticipantManager(db)
        self.__team_manager = TeamManager(db)
        self.__team_participant_manager = TeamParticipantManager(db)
        self.__validator = Validator(db)

        self.__participant_appended_to_team_message = "participant appended to team"
        self.__participant_deleted_team = "participant deleted from team"

    def append_participant_to_team(
            self,
            response: Response,
            token: str,
            participant_email: EmailStr,
            team_name: str,
    ) -> dict[str, str]:
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__validator.check_participant_and_team_existence(participant_email, team_name)
        self.check_ownership_for_not_admin(decoded_token, participant_email, team_name)

        participant = self.__participant_manager.read_by_email(participant_email)
        team = self.__team_manager.read_by_name(team_name)

        self.__team_participant_manager.raise_exception_if_participant_already_in_team(participant, team)
        self.__validator.raise_exception_if_team_default(team)
        self.__team_participant_manager.append_participant_to_team(participant, team)

        return {"message": self.__participant_appended_to_team_message}

    def check_ownership_for_not_admin(self, decoded_token: TokenDecodedSchema, participant_email: str, team_name: str):
        if decoded_token.role != UserRole.admin:
            self.__team_manager.raise_exception_if_owner_wrong(team_name, decoded_token.user_id)
            self.__participant_manager.raise_exception_if_owner_wrong(participant_email, decoded_token.user_id)

    def delete_participant_from_team(
            self,
            response: Response,
            token: str,
            participant_email: EmailStr,
            team_name: str
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__validator.check_participant_and_team_existence(participant_email, team_name)
        self.check_ownership_for_not_admin(decoded_token, participant_email, team_name)

        participant = self.__participant_manager.read_by_email(participant_email)
        team = self.__team_manager.read_by_name(team_name)

        self.__team_participant_manager.raise_exception_if_participant_not_in_team(participant, team)
        self.__validator.raise_exception_if_team_default(team)

        self.__team_participant_manager.delete_participant_from_team(participant_email, team_name)
        return {"message": self.__participant_deleted_team}
