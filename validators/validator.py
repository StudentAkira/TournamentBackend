from fastapi import HTTPException
from pydantic import EmailStr
from starlette import status

from db.crud.nomination_event import get_nomination_event_teams_db, get_nomination_event_db
from db.crud.participant import get_emails_of_teams_members_db
from db.crud.team import get_team_participants_emails_db, get_team_by_name_db
from db.schemas.team import TeamSchema
from db.schemas.token import TokenDecodedSchema
from db.schemas.user import UserRole
from managers.event import EventManager
from managers.nomination_event import NominationEventManager
from managers.nomination import NominationManager
from managers.participant import ParticipantManager
from managers.team import TeamManager


class Validator:
    def __init__(self, db):
        self.__participant_manager = ParticipantManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__event_manager = EventManager(db)
        self.__team_manager = TeamManager(db)
        self.__db = db

        self.__cant_append_participant_to_default_team_error = "you cant not append participant to default team"
        self.__participant_not_in_team_error = "participant not in team error"
        self.__team_already_in_nomination_event_error = "team already in nomination event"
        self.__participant_in_another_team_error = "participant in another team"
        self.__registration_finished_error = "Registration_finished"

    def check_team_event_nomination__nomination_event__existence(self,
                                                                 team_name: str,
                                                                 nomination_name: str,
                                                                 event_name: str
                                                                 ):
        self.__team_manager.raise_exception_if_team_not_found(team_name)
        self.check_event_nomination__nomination_event_existence(nomination_name, event_name)

    def check_event_nomination__nomination_event_existence(self,
                                                           nomination_name: str,
                                                           event_name: str
                                                           ):
        self.__event_manager.raise_exception_if_event_not_found(event_name)
        self.__nomination_manager.raise_exception_if_nomination_not_found(nomination_name)
        self.__nomination_event_manager.raise_exception_if_nomination_event_not_found(nomination_name, event_name)

    def check_if_team_not_in_event_nomination(
            self,
            team_name,
            nomination_name,
            event_name
    ):
        self.__nomination_event_manager.raise_exception_if_team_not_in_event_nomination(
            team_name,
            nomination_name,
            event_name
        )

    def validate_user_entity_ownership(self, decoded_token: TokenDecodedSchema, team_name: str, event_name: str):
        if decoded_token.role == UserRole.specialist or decoded_token.role == UserRole.judge:
            self.__team_manager.raise_exception_if_team_owner_wrong(team_name, decoded_token.user_id)
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_event_owner_wrong(event_name, decoded_token.user_id)

    def check_participant_and_team_existence(self, participant_email: EmailStr, team_name: str):
        self.__participant_manager.raise_exception_if_participant_not_found(participant_email)
        self.__team_manager.raise_exception_if_team_not_found(team_name)

    def raise_exception_if_team_default(self, team: TeamSchema):
        if "default_team" in team.name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__cant_append_participant_to_default_team_error}
            )

    def check_nomination_event__nomination_event_existence(self, nomination_name: str, event_name: str):
        self.__nomination_manager.raise_exception_if_nomination_not_found(nomination_name)
        self.__event_manager.raise_exception_if_event_not_found(event_name)
        self.__nomination_event_manager.raise_exception_if_nomination_event_not_found(nomination_name, event_name)

    def raise_exception_if_participants_in_team(self, team_name: str, participant_emails: list[EmailStr]):
        team_participants_emails = set(get_team_participants_emails_db(self.__db, team_name))
        participant_emails = set(participant_emails)
        if not participant_emails.issubset(team_participants_emails):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_not_in_team_error}
            )

    def raise_exception_if_team_already_in_nomination_event(self, team_name: str, nomination_name: str,
                                                            event_name: str):
        team_db = get_team_by_name_db(self.__db, team_name)
        teams_db = get_nomination_event_teams_db(self.__db, nomination_name, event_name)

        if team_db in teams_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__team_already_in_nomination_event_error}
            )

    def raise_exception_if_participant_in_another_team(self, team_name: str, nomination_name: str, event_name: str):

        team_db = get_team_by_name_db(self.__db, team_name)

        teams_db = get_nomination_event_teams_db(self.__db, nomination_name, event_name)
        participants_emails = set(get_emails_of_teams_members_db(teams_db))
        received_team_participant_emails = set(self.__team_manager.get_emails_of_team(team_db))

        if participants_emails & received_team_participant_emails:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_in_another_team_error}
            )

    def raise_exception_if_registration_finished(self, nomination_name: str, event_name: str):
        nomination_event_db = get_nomination_event_db(self.__db, nomination_name, event_name)
        if nomination_event_db.registration_finished:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error", self.__registration_finished_error}
            )
