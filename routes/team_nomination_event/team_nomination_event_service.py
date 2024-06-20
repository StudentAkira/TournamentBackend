from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event.nomination_event import NominationEventSchema
from db.schemas.user.user_role import UserRole
from managers.event import EventManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.team_nomination_event import TeamNominationEventManager
from managers.token import TokenManager
from utils.validation_util import Validator


class TeamNominationEventService:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__token_manager = TokenManager(db)
        self.__validator = Validator(db)
        self.__nomination_manager = NominationManager(db)
        self.__event_manager = EventManager(db)
        self.__nomination_event_manager = NominationEventManager(db)

        self.__team_nomination_event_manager = TeamNominationEventManager(db)

    def list_teams_nomination_event(
            self,
            response: Response,
            token: str,
            nomination_event: NominationEventSchema
    ) -> list:
        decoded_token = self.__token_manager.decode_token(token, response)

        nomination_db = self.__nomination_manager.get_by_name_and_user_id_or_raise_exception_if_not_found(
            decoded_token.user_id,
            nomination_event.nomination_name,
        )
        event_db = self.__event_manager.get_by_name_or_raise_if_not_found(nomination_event.event_name)
        nomination_event_db = self.__nomination_event_manager.get_nomination_event_or_raise_if_not_found(
            nomination_db, event_db, nomination_event.type
        )
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_owner_wrong(event_db, decoded_token.user_id)

        return self.__team_nomination_event_manager.list_teams_of_nomination_event(nomination_event_db)
