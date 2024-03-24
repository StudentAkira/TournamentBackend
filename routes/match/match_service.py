from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.match import SetMatchResultSchema
from db.schemas.nomination_event import NominationEventSchema
from managers.event import EventManager
from managers.match import MatchManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.team import TeamManager
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
        self.__team_manager = TeamManager(db)

        self.__match_result_set_message = "match result set"

    def set_match_result(self, response: Response, token: str, data: SetMatchResultSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__event_manager.raise_exception_if_not_found(data.nomination_event.event_name)
        self.__nomination_manager.raise_exception_if_not_found(data.nomination_event.nomination_name)
        self.__nomination_event_manager.raise_exception_if_not_found(
            data.nomination_event.nomination_name,
            data.nomination_event.event_name,
            data.nomination_event.type
        )
        data.winner_team_name = self.__team_manager.get_team_name_from_team_name_or_participant_email(
            data.winner_team_name
        )
        self.__event_manager.raise_exception_if_user_not_in_judge_command(
            data.nomination_event.nomination_name,
            data.nomination_event.event_name,
            data.nomination_event.type,
            decoded_token.user_id
        )
        self.__match_manager.raise_exception_if_not_found(data.match_id)
        self.__match_manager.raise_exception_if_match_not_related_to_nomination_event(data)
        self.__match_manager.raise_exception_if_winner_not_in_match(data.match_id, data.winner_team_name)

        self.__match_manager.set_match_result(decoded_token.user_id, data)
        return {"message": self.__match_result_set_message}

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
        self.__nomination_event_manager.raise_exception_if_nomination_event_not_olympyc(nomination_event.type)

        return self.__match_manager.get_group_matches_of_tournament(nomination_event)
