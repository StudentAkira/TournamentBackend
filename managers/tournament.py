from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.nomination_event.nomination_event import close_registration_nomination_event_db
from db.crud.team.team import team_check_existence_in_tournament_db
from db.crud.tournament.tournaments import get_groups_of_tournament_db, get_count_of_participants_of_tournament_db, \
    is_all_matches_finished_db, \
    finish_group_stage_db, start_play_off_tournament_db, finish_play_off_stage_db, start_group_stage_db
from db.models.nomination_event import NominationEvent
from db.schemas.group_tournament.start_group_tournament import StartGroupTournamentSchema
from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema
from db.schemas.team.team import TeamSchema


class TournamentManager:
    __db: Session

    def __init__(self, db):
        self.__db = db

        self.__invalid_group_count_error = "invalid group count"
        self.__not_all_matches_finished_error = "not all matches are finished"
        self.__group_stage_not_finished_error = "group stage is not finished"
        self.__group_stage_finished_error = "group stage is finished"
        self.__group_stage_already_finished_error = "group stage is already finished"
        self.__top_count_wrong_error = "top count parameter is wrong"
        self.__wrong_teams_provided = "wrong teams provided"
        self.__play_off_stage_already_started = "play off stage already started"
        self.__play_off_stage_not_finished_error = "play off stage not finished"
        self.__play_off_stage_already_finished_error = "play off stage already finished"
        self.__play_off_stage_not_started = "play off stage not started"

    def start_group_stage(
            self,
            nomination_event_db: type(NominationEvent),
            group_count: int
    ):
        close_registration_nomination_event_db(
            self.__db,
            nomination_event_db
       )
        self.validate_group_count(group_count, nomination_event_db)
        start_group_stage_db(self.__db, nomination_event_db, group_count)

    def get_groups_of_tournament(self, nomination_event_db: type(NominationEvent)):
        return get_groups_of_tournament_db(nomination_event_db)

    def finish_group_stage(self, nomination_event_db):
        finish_group_stage_db(self.__db, nomination_event_db)

    def start_play_off_tournament(self, nomination_event_db: type(NominationEvent), teams: list[TeamSchema]):
        start_play_off_tournament_db(self.__db, nomination_event_db, teams)

    def finish_play_off_stage(self, nomination_event_db):
        finish_play_off_stage_db(self.__db, nomination_event_db)

    def validate_group_count(self, group_count: int, nomination_event_db: type(NominationEvent)):
        team_count = get_count_of_participants_of_tournament_db(nomination_event_db)
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

    def raise_exception_if_not_all_matches_finished(self, nomination_event_db: type(NominationEvent)):
        all_matches_finished = is_all_matches_finished_db(self.__db, nomination_event_db)
        if not all_matches_finished:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__not_all_matches_finished_error}
            )

    def raise_exception_if_group_stage_not_finished(self, nomination_event_db: type(NominationEvent)):
        if not nomination_event_db.group_stage_finished:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__group_stage_not_finished_error}
            )

    def raise_exception_if_group_stage_finished(self, nomination_event_db: type(NominationEvent)):
        print(type(nomination_event_db))
        if nomination_event_db.group_stage_finished:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__group_stage_finished_error}
            )

    def raise_exception_if_teams_not_in_tournament(
            self,
            teams: list[TeamSchema],
            nomination_event_db: type(NominationEvent)
    ):
        teams_in_tournament = team_check_existence_in_tournament_db(self.__db, teams, nomination_event_db)
        if not teams_in_tournament:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__wrong_teams_provided}
            )

    def raise_exception_if_play_off_stage_started(self, nomination_event_db: type(NominationEvent)):
        if nomination_event_db.bracket is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__play_off_stage_already_started}
            )

    def raise_exception_if_play_off_stage_not_started(self, nomination_event_db: type(NominationEvent)):
        if nomination_event_db.bracket is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__play_off_stage_not_started}
            )

    def raise_exception_if_play_off_stage_finished(self, nomination_event_db: type(NominationEvent)):
        if nomination_event_db.play_off_stage_finished:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__play_off_stage_already_finished_error}
            )
