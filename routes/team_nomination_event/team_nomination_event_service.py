from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.user import UserRole
from managers.event import EventManager
from managers.team_nomination_event import TeamNominationEventManager
from managers.token import TokenManager
from validators.validator import Validator


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
            nomination_name: str,
            event_name: str,
    ) -> list:
        decoded_token = self.__token_manager.decode_token(token, response)

        self.__validator.check_event_nomination__nomination_event_existence(nomination_name, event_name)
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_owner_wrong(event_name, decoded_token.user_id)

        return self.__team_nomination_event_manager.list_teams_of_nomination_event(nomination_name, event_name)
