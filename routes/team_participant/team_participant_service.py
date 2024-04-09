from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.models.participant import Participant
from db.models.team import Team
from db.schemas.token.token_decoded import TokenDecodedSchema
from db.schemas.user.user_role import UserRole
from managers.participant import ParticipantManager
from managers.team import TeamManager
from managers.team_participant import TeamParticipantManager
from managers.token import TokenManager
from utils.validation_util import Validator


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
        team_name = self.__team_manager.get_team_name_from_team_name_or_participant_email(team_name)

        team_db = self.__team_manager.get_by_name_or_raise_if_not_found(team_name)
        participant_db = self.__participant_manager.get_by_email_or_raise_if_not_found(participant_email)

        self.check_ownership_for_not_admin(decoded_token, participant_db, team_db)

        self.__team_participant_manager.raise_exception_if_participant_already_in_team(participant_db, team_db)
        self.__team_manager.raise_exception_if_team_default(team_db.name)
        self.__team_participant_manager.append_participant_to_team(participant_db, team_db)
        return {"message": self.__participant_appended_to_team_message}

    def check_ownership_for_not_admin(
            self,
            decoded_token: TokenDecodedSchema,
            participant_db: type(Participant),
            team_db: type(Team)
    ):
        if decoded_token.role != UserRole.admin:
            self.__team_manager.raise_exception_if_owner_wrong(team_db, decoded_token.user_id)
            self.__participant_manager.raise_exception_if_owner_wrong(participant_db, decoded_token.user_id)
