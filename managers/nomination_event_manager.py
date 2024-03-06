from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.nomination_event import get_nomination_event_db, get_nomination_events_full_info_db, \
    get_nomination_events_full_info_by_owner_db, get_nomination_events_names_db, get_nomination_events_names_by_owner_db
from db.crud.team import get_teams_by_event_nomination_db, get_team_by_name_db, append_team_to_nomination_event_db
from db.schemas.nomination_event import NominationEventSchema, NominationEventNameSchema
from db.schemas.team import TeamSchema
from managers.team_manager import TeamManager


class NominationEventManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__team_manager = TeamManager(db)

        self.__nomination_event_does_not_exist_error = "nomination event does not exist"
        self.__team_already_in_nomination_event_error = "team already in nomination event"
        self.__participant_in_another_team_error = "participant found in another team of nomination event"
        self.__team_not_in_nomination_event_error = "team not in event nomination error"

    def get_nominations_events_names(self, offset: int, limit: int) -> list[NominationEventNameSchema]:
        nominations_events = get_nomination_events_names_db(self.__db, offset, limit)
        return nominations_events

    def get_nominations_events_names_by_owner(
            self, offset: int, limit: int, owner_id: int) -> list[NominationEventNameSchema]:
        nominations_events = get_nomination_events_names_by_owner_db(self.__db, offset, limit, owner_id)
        return nominations_events

    def get_nominations_events_full_info(self, offset: int, limit: int) -> list[NominationEventSchema]:
        nominations_events = get_nomination_events_full_info_db(self.__db, offset, limit)
        return nominations_events

    def get_nominations_events_full_info_by_owner(
            self, offset: int, limit: int, owner_id: int) -> list[NominationEventSchema]:
        nominations_events = get_nomination_events_full_info_by_owner_db(self.__db, offset, limit, owner_id)
        return nominations_events

    def get_teams_of_nomination_event(self, nomination_name: str, event_name: str) -> list[TeamSchema]:
        teams_db = get_teams_by_event_nomination_db(self.__db, nomination_name, event_name)
        teams = [TeamSchema.from_orm(team_db) for team_db in teams_db]
        return teams

    def append_team_to_event_nomination(self, team_name: str, nomination_name: str, event_name: str):
        append_team_to_nomination_event_db(self.__db, team_name, nomination_name, event_name)

    def get_emails_of_all_participants_in_event_nomination(self, event_name, nomination_name):
        teams_db = get_teams_by_event_nomination_db(self.__db, nomination_name, event_name)
        emails = set()
        for team_db in teams_db:
            emails.union(self.__team_manager.get_emails_of_team(team_db))
        return emails

    def get_participant_emails_of_nomination_event(self, nomination_name: str, event_name: str):
        teams_db = get_teams_by_event_nomination_db(self.__db, nomination_name, event_name)
        nomination_event_participant_emails = set()
        for team_db in teams_db:
            for participant_db in team_db.participants:
                nomination_event_participant_emails.add(participant_db.email)
        return nomination_event_participant_emails

    def raise_exception_if_nomination_event_not_found(self, nomination_name: str, event_name: str):
        nomination_event = get_nomination_event_db(self.__db, nomination_name,  event_name)
        if not nomination_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__nomination_event_does_not_exist_error}
            )

    def raise_exception_if_team_already_in_nomination_event(
            self,
            team_name: str,
            nomination_name: str,
            event_name: str
    ):
        teams_names = set(team.name for team in self.get_teams_of_nomination_event(nomination_name, event_name))
        if team_name in teams_names:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_already_in_nomination_event_error}
            )

    def raise_exception_if_participant_already_in_nomination_event(
            self,
            team_name: str,
            nomination_name: str,
            event_name: str
    ):
        received_team_db = get_team_by_name_db(self.__db, team_name)
        received_team_participants_emails = set(
            participant.email for participant in received_team_db.participants
        )
        nomination_event_participant_emails = self.get_participant_emails_of_nomination_event(
            nomination_name,
            event_name
        )
        self.check_emails_intersection(nomination_event_participant_emails, received_team_participants_emails)

    def check_emails_intersection(self, intersectable, intersecting):
        if len(intersectable.intersection(intersecting)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_in_another_team_error}
            )

    def raise_exception_if_team_not_in_event_nomination(self, team_name: str, nomination_name: str, event_name: str):
        teams_names = set(team.name for team in self.get_teams_of_nomination_event(nomination_name, event_name))
        if team_name not in teams_names:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_not_in_nomination_event_error}
            )
