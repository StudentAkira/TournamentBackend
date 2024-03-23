from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event import NominationEventSchema
from managers.event import EventManager
from managers.match import MatchManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.token import TokenManager


class MatchService:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__event_manager = EventManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__token_manager = TokenManager(db)
        self.__match_manager = MatchManager(db)

    def get_group_matches_of_tournament(
            self,
            response: Response,
            token: str,
            nomination_event: NominationEventSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__event_manager.raise_exception_if_not_found(nomination_event.event_name)
        self.__nomination_manager.raise_exception_if_not_found(nomination_event.nomination_name)
        self.__nomination_event_manager.raise_exception_if_not_found(
            nomination_event.nomination_name,
            nomination_event.event_name,
            nomination_event.type
        )

        self.__event_manager.raise_exception_if_owner_wrong(nomination_event.event_name, decoded_token.user_id)

        return self.__match_manager.get_group_matches_of_tournament(nomination_event)
