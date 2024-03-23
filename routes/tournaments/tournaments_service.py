from starlette.responses import Response

from db.schemas.group_tournament import StartGroupTournamentSchema
from db.schemas.nomination_event import NominationEventSchema
from managers.event import EventManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.token import TokenManager
from managers.tournament import TournamentManager


class TournamentService:

    def __init__(self, db):
        self.__db = db

        self.__event_manager = EventManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__token_manager = TokenManager(db)
        self.__tournament_manager = TournamentManager(db)

        self.__groups_created_message = "Groups created"

    def create_group_tournament(self, response: Response, token: str, nomination_event: StartGroupTournamentSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__nomination_manager.raise_exception_if_not_found(nomination_event.nomination_name)
        self.__event_manager.raise_exception_if_not_found(nomination_event.event_name)
        self.__nomination_event_manager.raise_exception_if_not_found(
            nomination_event.nomination_name,
            nomination_event.event_name,
            nomination_event.type
        )

        self.__event_manager.raise_exception_if_owner_wrong(nomination_event.event_name, decoded_token.user_id)
        self.__nomination_event_manager.raise_exception_if_tournament_started(
            nomination_event.nomination_name,
            nomination_event.event_name,
            nomination_event.type
        )
        self.__tournament_manager.create_group_tournament(nomination_event)
        return {"message": self.__groups_created_message}

    def get_groups_of_tournament(self, response: Response, token: str, nomination_event: NominationEventSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__nomination_manager.raise_exception_if_not_found(nomination_event.nomination_name)
        self.__event_manager.raise_exception_if_not_found(nomination_event.event_name)
        self.__nomination_event_manager.raise_exception_if_not_found(
            nomination_event.nomination_name,
            nomination_event.event_name,
            nomination_event.type
        )
        self.__event_manager.raise_exception_if_owner_wrong(nomination_event.event_name, decoded_token.user_id)
        return self.__tournament_manager.get_groups_of_tournament(nomination_event)
