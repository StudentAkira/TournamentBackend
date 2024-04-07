from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event.nomination_event import NominationEventSchema
from db.schemas.user.user_role import UserRole
from managers.event import EventManager
from managers.team_nomination_event import TeamNominationEventManager
from managers.token import TokenManager
from utils.validation_util import Validator


class TeamNominationEventService:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__token_manager = TokenManager(db)
        self.__validator = Validator(db)
        self.__event_manager = EventManager(db)
        self.__team_nomination_event_manager = TeamNominationEventManager(db)

    def list_teams_nomination_event(
            self,
            response: Response,
            token: str,
            nomination_event: NominationEventSchema
    ) -> list:
        decoded_token = self.__token_manager.decode_token(token, response)

        self.__validator.check_event_nomination__nomination_event_existence(
            nomination_event.nomination_name,
            nomination_event.event_name,
            nomination_event.nomination_event_type
        )
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_owner_wrong(nomination_event.event_name, decoded_token.user_id)

        return self.__team_nomination_event_manager.list_teams_of_nomination_event(nomination_event)
