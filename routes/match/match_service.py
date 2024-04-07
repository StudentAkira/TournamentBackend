from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.match.set_match_result_schema import SetMatchResultSchema
from db.schemas.nomination_event.nomination_event_type import NominationEventType
from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema
from managers.event import EventManager
from managers.match import MatchManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.team import TeamManager
from managers.token import TokenManager
from managers.tournament import TournamentManager
from utils.validation_util import Validator


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
        self.__tournament_manger = TournamentManager(db)

        self.__validator = Validator(db)

        self.__match_result_set_message = "match result set"

    def set_group_match_result(self, response: Response, token: str, data: SetMatchResultSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__validator.validate_event_nomination__nomination_event_existence(
            data.nomination_event.nomination_name,
            data.nomination_event.event_name,
            NominationEventType.olympyc
        )
        self.__match_manager.raise_exception_if_not_found(data.match_id)
        self.__match_manager.raise_exception_if_match_not_related_to_nomination_event(data)
        self.__tournament_manger.raise_exception_if_group_stage_finished(data.nomination_event)

        if data.winner_team_name:
            self.__match_manager.raise_exception_if_winner_not_in_match(data.match_id, data.winner_team_name)

        self.__match_manager.set_group_match_result(decoded_token.user_id, data)
        return {"message": self.__match_result_set_message}

    def set_bracket_match_result(self, response: Response, token: str, data: SetMatchResultSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__validator.validate_event_nomination__nomination_event_existence(
            data.nomination_event.nomination_name,
            data.nomination_event.event_name,
            NominationEventType.olympyc
        )
        self.__match_manager.raise_exception_if_not_found(data.match_id)
        self.__match_manager.raise_exception_if_match_not_related_to_nomination_event(data)
        self.__match_manager.raise_exception_if_no_winner_in_bracket_match(data)
        self.__tournament_manger.raise_exception_if_play_off_stage_finished(data.nomination_event)
        self.__match_manager.raise_exception_if_winner_not_in_match(data.match_id, data.winner_team_name)
        self.__match_manager.raise_exception_if_prev_match_was_not_judged(data)
        self.__match_manager.set_bracket_match_result(decoded_token.user_id, data)
        return {"message": self.__match_result_set_message}

    def get_group_matches(
            self,
            response: Response,
            token: str,
            nomination_event: OlympycNominationEventSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__validator.validate_event_nomination__nomination_event_existence(
            nomination_event.nomination_name,
            nomination_event.event_name,
            NominationEventType.olympyc
        )
        self.__event_manager.raise_exception_if_owner_wrong(nomination_event.event_name, decoded_token.user_id)
        return self.__match_manager.get_group_matches(nomination_event)

    def get_bracket_matches(
            self,
            response: Response,
            token: str,
            nomination_event: OlympycNominationEventSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__validator.validate_event_nomination__nomination_event_existence(
            nomination_event.nomination_name,
            nomination_event.event_name,
            NominationEventType.olympyc
        )
        self.__tournament_manger.raise_exception_if_play_off_stage_not_started(nomination_event)
        self.__event_manager.raise_exception_if_owner_wrong(nomination_event.event_name, decoded_token.user_id)
        return self.__match_manager.get_bracket_matches(nomination_event)
