from typing import cast

from fastapi import HTTPException
from sqlalchemy import exists, or_
from sqlalchemy.orm import Session
from starlette import status

from db.crud.match import get_group_matches_db, \
    is_match_related_to_nomination_event_db, get_bracket_matches_db, set_group_match_result_db, \
    is_winner_exists_in_bracket_match_db, set_bracket_match_result_db
from db.models.match import Match
from db.models.team import Team
from db.schemas.match import SetMatchResultSchema
from db.schemas.nomination_event import OlympycNominationEventSchema
from managers.team import TeamManager


class MatchManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__team_manager = TeamManager(db)

        self.__match_not_related_to_group_error = "match not related to group"
        self.__match_not_found_error = "match not found error"
        self.__team_not_related_to_match_error = "team not related to match error"
        self.__wrong_match_data_error = "wrong match data error"
        self.__play_off_matches_cannot_result_draw = "play off match cannot be draw"

    def get_group_matches(self, nomination_event: OlympycNominationEventSchema):
        data = get_group_matches_db(self.__db, nomination_event)
        return data

    def get_bracket_matches(self, nomination_event: OlympycNominationEventSchema):
        data = get_bracket_matches_db(self.__db, nomination_event)
        return data

    def set_group_match_result(self, judge_id: int, data: SetMatchResultSchema):
        set_group_match_result_db(self.__db, judge_id, data)

    def set_bracket_match_result(self, judge_id, data):
        set_bracket_match_result_db(self.__db, judge_id, data)

    def raise_exception_if_match_not_related_to_nomination_event(self, data: SetMatchResultSchema):
        is_match_related = is_match_related_to_nomination_event_db(self.__db, data)
        if not is_match_related:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__match_not_related_to_group_error}
            )

    def raise_exception_if_not_found(self, match_id: int):
        entity_exists = self.__db.query(
            exists(

            ).where(
                cast("ColumnElement[bool]", Match.id == match_id)
            )
        ).scalar()

        if not entity_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__match_not_found_error}
            )

    def raise_exception_if_winner_not_in_match(self, match_id: int, winner_team_name: str):

        team_db = self.__db.query(Team).filter(cast("ColumnElement[bool]", Team.name == winner_team_name)).first()

        entity_exists = self.__db.query(
            exists(

            ).where(
                cast("ColumnElement[bool]", Match.id == match_id)
            ).where(or_(
                Match.team1_id == team_db.id,
                Match.team2_id == team_db.id
                )
            )
        ).scalar()
        if not entity_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_not_related_to_match_error}
            )

    def raise_exception_if_no_winner_in_bracket_match(self, data: SetMatchResultSchema):
        winner_exists_in_bracket_match = is_winner_exists_in_bracket_match_db(self.__db, data)
        if not winner_exists_in_bracket_match:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error", self.__play_off_matches_cannot_result_draw}
            )

