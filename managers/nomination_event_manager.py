from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.testing import combinations
from starlette import status

from db.crud.nomination_event import get_nomination_event_db, get_nomination_events_full_info_db, \
    get_nomination_events_all_names_by_owner_db, \
    get_nomination_events_full_info_by_owner_db, get_nomination_event_teams_db, get_nomination_events_all_names_db, \
    finish_event_nomination_registration_db, get_list_events_list_nominations_db, \
    get_list_events_list_nominations_by_owner_db
from db.crud.team import get_team_by_name_db, append_team_to_nomination_event_db
from db.schemas.nomination_event import NominationEventSchema, NominationEventNameSchema
from db.schemas.team import TeamSchema, TeamToEventNominationSchema
from managers.team_manager import TeamManager


class NominationEventManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__team_manager = TeamManager(db)

        self.__nomination_event_does_not_exist_error = "nomination event does not exist"
        self.__team_not_in_nomination_event_error = "team not in event nomination error"
        self.__tournament_already_started_error = "tournament already started"

    def get_nominations_events_names(self, offset: int, limit: int) -> list[NominationEventNameSchema]:
        nominations_events = get_nomination_events_all_names_db(self.__db, offset, limit)
        return nominations_events

    def get_nominations_events_names_by_owner(
            self, offset: int, limit: int, owner_id: int) -> list[NominationEventNameSchema]:
        nominations_events = get_nomination_events_all_names_by_owner_db(self.__db, offset, limit, owner_id)
        return nominations_events

    def get_nominations_events_full_info(self, offset: int, limit: int) -> list[NominationEventSchema]:
        nominations_events = get_nomination_events_full_info_db(self.__db, offset, limit)
        return nominations_events

    def get_nominations_events_full_info_by_owner(
            self, offset: int, limit: int, owner_id: int) -> list[NominationEventSchema]:
        nominations_events = get_nomination_events_full_info_by_owner_db(self.__db, offset, limit, owner_id)
        return nominations_events

    def get_teams_of_nomination_event(self, nomination_name: str, event_name: str) -> list[TeamSchema]:
        teams_db = get_nomination_event_teams_db(self.__db, nomination_name, event_name)
        teams = [TeamSchema.from_orm(team_db) for team_db in teams_db]
        return teams

    def get_list_events_list_nominations(self):
        return get_list_events_list_nominations_db(self.__db)

    def get_list_events_list_nominations_by_owner(self, owner_id: int):
        return get_list_events_list_nominations_by_owner_db(self.__db, owner_id)

    def append_team_to_event_nomination(
            self,
            team_nomination_event_data: TeamToEventNominationSchema
    ):
        append_team_to_nomination_event_db(self.__db, team_nomination_event_data)

    def finish_event_nomination_registration(self, nomination_name: str, event_name: str):
        self.raise_exception_if_tournament_already_started(nomination_name, event_name)
        finish_event_nomination_registration_db(self.__db, nomination_name, event_name)

    def get_nomination_event_group_stage(self, nomination_name: str, event_name: str):
        teams_db = get_nomination_event_teams_db(self.__db, nomination_name, event_name)
        teams = set(TeamSchema.from_orm(team_db) for team_db in teams_db)
        teams_combinations = combinations(teams)

    def raise_exception_if_nomination_event_not_found(self, nomination_name: str, event_name: str):
        nomination_event = get_nomination_event_db(self.__db, nomination_name,  event_name)
        if not nomination_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__nomination_event_does_not_exist_error}
            )

    def raise_exception_if_team_not_in_event_nomination(self, team_name: str, nomination_name: str, event_name: str):
        team_db = get_team_by_name_db(self.__db, team_name)
        teams_db = get_nomination_event_teams_db(self.__db, nomination_name, event_name)

        if team_db not in teams_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_not_in_nomination_event_error}
            )

    def raise_exception_if_tournament_already_started(self, nomination_name: str, event_name: str):
        nomination_event_db = get_nomination_event_db(self.__db, nomination_name, event_name)
        if nomination_event_db.registration_finished:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__tournament_already_started_error}
            )
