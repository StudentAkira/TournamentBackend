from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.match.match import get_group_matches_db, set_group_match_result_db, get_bracket_matches_db, \
    set_bracket_match_result_db, is_match_related_to_nomination_event_db, \
    is_prev_match_was_judged_db, get_match_by_id
from db.models.match import Match
from db.models.nomination_event import NominationEvent
from db.models.team import Team
from db.models.user import User
from db.schemas.match.set_group_match_result_schema import SetGroupMatchResultSchema
from managers.team import TeamManager


class MatchManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__team_manager = TeamManager(db)

        self.__match_not_related_to_group_error = "match not related to group"
        self.__match_not_found_error = "match not found"
        self.__team_not_related_to_match_error = "team not related to match"
        self.__wrong_match_data_error = "wrong match data"
        self.__play_off_matches_cannot_result_draw = "play off match cannot be draw"
        self.__prev_matches_not_finished = "prev matches not finished"

    def get_group_match_or_raise_if_not_found(self, match_id: int) -> type(Match):
        match_db = get_match_by_id(self.__db, match_id)
        if not match_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__match_not_found_error}
            )
        return match_db

    def get_group_matches(self, nomination_event_db: type(NominationEvent)):
        data = get_group_matches_db(nomination_event_db)
        return data

    def get_bracket_matches(self, nomination_event_db: type(NominationEvent)):
        data = get_bracket_matches_db(nomination_event_db)
        return data

    def set_group_match_result(self, judge_db: type(User), match_db: type(Match), data: SetGroupMatchResultSchema):
        set_group_match_result_db(self.__db, judge_db, match_db, data)

    def set_bracket_match_result(self, judge_db: type(User), match_db: type(Match), winner_team_db: type(Team)):
        set_bracket_match_result_db(self.__db, judge_db, match_db, winner_team_db)

    def raise_exception_if_match_not_related_to_nomination_event(
            self,
            nomination_event_db: type(NominationEvent),
            match_db: type(Match)
    ):
        is_match_related = is_match_related_to_nomination_event_db(nomination_event_db, match_db)
        if not is_match_related:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__match_not_related_to_group_error}
            )

    def raise_exception_if_winner_not_in_match(self, match_db: type(Match), winner_team_db: type(Team)):
        if winner_team_db is not None and match_db.team1 != winner_team_db and match_db.team2 != winner_team_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_not_related_to_match_error}
            )

    def raise_exception_if_prev_match_was_not_judged(
            self,
            nomination_event_db: type(NominationEvent),
            match_db: type(Match)
    ):
        prev_match_was_judged = is_prev_match_was_judged_db(nomination_event_db, match_db)
        if not prev_match_was_judged:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__prev_matches_not_finished}
            )
