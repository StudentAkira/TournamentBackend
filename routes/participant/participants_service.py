from pydantic import EmailStr
from starlette.responses import Response

from db.schemas.participant import ParticipantSchema, ParticipantHideSchema
from db.schemas.token import TokenDecodedSchema
from db.schemas.user import UserRole
from managers.participant import ParticipantManager
from managers.team import TeamManager
from managers.team_participant import TeamParticipantManager
from managers.token import TokenManager
from validators.validator import Validator


class ParticipantsService:

    def __init__(self, db):
        self.__db = db

        self.__token_manager = TokenManager(db)
        self.__participant_manager = ParticipantManager(db)
        self.__team_manager = TeamManager(db)
        self.__team_participant = TeamParticipantManager(db)
        self.__validator = Validator(db)

        self.__participant_created_message = "participant created"
        self.__participant_updated_message = "participant updated"
        self.__participant_hidden_message = "participant hidden"

    def list_by_owner(
            self,
            response: Response,
            token: str,
            offset: int,
            limit: int
    ) -> list[ParticipantSchema]:
        decoded_token = self.__token_manager.decode_token(token, response)
        return self.__participant_manager.list_by_owner(offset, limit, decoded_token.user_id)

    def create(self, response: Response, token: str, participant: ParticipantSchema) -> dict[str, str]:
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__participant_manager.create(participant, decoded_token.user_id)
        return {"message": self.__participant_created_message}

    def hide(self, response: Response, token: str, participant_data: ParticipantHideSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__participant_manager.raise_exception_if_not_found(participant_data.participant_email)
        self.__participant_manager.raise_exception_if_owner_wrong(
            participant_data.participant_email, decoded_token.user_id
        )
        self.__participant_manager.hide(participant_data)
        return {"message": self.__participant_hidden_message}
