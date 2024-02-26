from starlette.responses import Response

from db.schemas.participant import ParticipantSchema
from managers.paticipant_manager import ParticipantManager
from managers.token_manager import TokenManager


class ParticipantsService:

    def __init__(self, db):
        self.__db = db

        self.__token_manager = TokenManager(db)
        self.__participant_manager = ParticipantManager(db)

        self.__participant_created_message = "participant created"

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
