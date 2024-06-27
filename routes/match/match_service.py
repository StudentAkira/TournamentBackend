from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.match.set_group_match_result_schema import SetGroupMatchResultSchema
from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema
from managers.event import EventManager
from managers.match import MatchManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.team import TeamManager
from managers.token import TokenManager
from managers.tournament import TournamentManager
from utils.retriever_util import Retriever
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
        self.__retriever = Retriever(db)

        self.__match_result_set_message = "match result set"

    def set_group_match_result(self, response: Response, token: str, data: SetGroupMatchResultSchema):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event(
                response,
                token,
                data.nomination_event.to_nomination_event_schema()
            )
        match_db = self.__match_manager.get_group_match_or_raise_if_not_found(data.match_id)
        self.__match_manager.raise_exception_if_match_not_related_to_nomination_event(nomination_event_db, match_db)
        self.__tournament_manger.raise_exception_if_group_stage_finished(nomination_event_db)
        self.__match_manager.set_group_match_result(user_db, match_db, data)
        return {"message": self.__match_result_set_message}

    def set_bracket_match_result(self, response: Response, token: str, data: SetGroupMatchResultSchema):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event(
                response,
                token,
                data.nomination_event.to_nomination_event_schema()
            )
        match_db = self.__match_manager.get_group_match_or_raise_if_not_found(data.match_id)
        if data.winner_team_name:
            team_db = self.__team_manager.get_by_name_or_raise_if_not_found(data.winner_team_name)
        else:
            team_db = None
        self.__match_manager.raise_exception_if_match_not_related_to_nomination_event(nomination_event_db, match_db)
        self.__match_manager.raise_exception_if_winner_not_in_match(match_db, team_db)
        self.__tournament_manger.raise_exception_if_play_off_stage_finished(nomination_event_db)
        self.__tournament_manger.raise_exception_if_play_off_stage_not_started(nomination_event_db)
        self.__match_manager.raise_exception_if_prev_match_was_not_judged(nomination_event_db, match_db)
        self.__match_manager.set_bracket_match_result(user_db, match_db, team_db)
        return {"message": self.__match_result_set_message}

    def get_group_matches(
            self,
            response: Response,
            token: str,
            nomination_event: OlympycNominationEventSchema
    ):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event(
                response,
                token,
                nomination_event.to_nomination_event_schema()
            )
        self.__event_manager.raise_exception_if_owner_wrong(event_db, user_db.id)
        return self.__match_manager.get_group_matches(nomination_event_db)

    def get_bracket_matches(
            self,
            response: Response,
            token: str,
            nomination_event: OlympycNominationEventSchema
    ):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event(
                response,
                token,
                nomination_event.to_nomination_event_schema()
            )
        self.__tournament_manger.raise_exception_if_play_off_stage_not_started(nomination_event_db)
        self.__event_manager.raise_exception_if_owner_wrong(event_db, user_db.id)
        return self.__match_manager.get_bracket_matches(nomination_event_db)
