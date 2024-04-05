from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.nomination_event import close_registration_nomination_event_db, is_group_stage_finished_db
from db.crud.team import team_check_existence_in_tournament_db
from db.crud.tournaments import create_group_tournament_db, \
    get_groups_of_tournament_db, get_count_of_participants_of_tournament_db, is_all_matches_finished_db, \
    finish_group_stage_db, start_play_off_tournament_db
from db.schemas.group_tournament import StartGroupTournamentSchema
from db.schemas.match import SetMatchResultSchema
from db.schemas.nomination_event import NominationEventSchema
from db.schemas.team import TeamSchema


class TournamentManager:
    __db: Session

    def __init__(self, db):
        self.__db = db

        self.__invalid_group_count_error = "invalid group count"
        self.__not_all_matches_finished_error = "not all matches are finished"
        self.__group_stage_not_finished_error = "group stage is not finished"
        self.__group_stage_finished_error = "group stage is finished"
        self.__top_count_wrong_error = "top count parameter is wrong"
        self.__wrong_teams_provided = "wrong teams provided"

    def create_group_tournament(self, nomination_event: StartGroupTournamentSchema):
        close_registration_nomination_event_db(self.__db, NominationEventSchema(
            **nomination_event.model_dump()
        ))
        self.validate_group_count(
            nomination_event.group_count,
            nomination_event.nomination_name,
            nomination_event.event_name,
            nomination_event.type
        )
        create_group_tournament_db(self.__db, nomination_event)

    def get_groups_of_tournament(self, nomination_event: NominationEventSchema):
        return get_groups_of_tournament_db(self.__db, nomination_event)

    def finish_group_stage(self, nomination_event):
        finish_group_stage_db(self.__db, nomination_event)

    def start_play_off_tournament(self, nomination_event: NominationEventSchema, teams: list[TeamSchema]):
        start_play_off_tournament_db(self.__db, nomination_event, teams)

    def validate_group_count(self, group_count: int, nomination_name: str, event_name: str, nomination_event_type: str):
        team_count = get_count_of_participants_of_tournament_db(
            self.__db,
            nomination_name,
            event_name,
            nomination_event_type
        )
        max_group_amount = int(team_count / 2)
        if team_count <= 3 and group_count >= 2:
            self.raise_exception_if_group_count_wrong()
        if group_count > team_count:
            self.raise_exception_if_group_count_wrong()
        if group_count > max_group_amount:
            self.raise_exception_if_group_count_wrong()

    def raise_exception_if_group_count_wrong(self):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": self.__invalid_group_count_error}
        )

    def raise_exception_if_not_all_matches_finished(self, nomination_event: NominationEventSchema):
        all_matches_finished = is_all_matches_finished_db(self.__db, nomination_event)
        if not all_matches_finished:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__not_all_matches_finished_error}
            )

    def raise_exception_if_group_stage_not_finished(self, nomination_event: NominationEventSchema):
        if not is_group_stage_finished_db(self.__db, nomination_event):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__group_stage_not_finished_error}
            )

    def raise_exception_if_group_stage_finished(self, data: SetMatchResultSchema):
        group_stage_finished = is_group_stage_finished_db(self.__db, data.nomination_event)
        if group_stage_finished:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__group_stage_finished_error}
            )

    def raise_exception_if_teams_not_in_tournament(
            self,
            teams: list[TeamSchema],
            nomination_event: NominationEventSchema
    ):
        teams_in_tournament = team_check_existence_in_tournament_db(self.__db, teams, nomination_event)
        if not teams_in_tournament:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__wrong_teams_provided}
            )


