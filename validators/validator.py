from fastapi import HTTPException
from pydantic import EmailStr
from starlette import status

from db.crud.nomination_event import get_nomination_event_db
from db.crud.participant_nomination_event import get_participants_of_nomination_event_db
from db.crud.team import get_team_participants_emails_db, get_team_by_name_db
from db.crud.team_nomination_event import get_nomination_event_teams_db
from db.crud.team_participant import get_emails_of_teams_participants_db
from db.schemas.team import TeamSchema
from db.schemas.token import TokenDecodedSchema
from db.schemas.user import UserRole
from managers.event import EventManager
from managers.nomination_event import NominationEventManager
from managers.nomination import NominationManager
from managers.participant import ParticipantManager
from managers.team import TeamManager
from managers.team_nomination_event import TeamNominationEventManager


class Validator:
    def __init__(self, db):
        self.__team_nomination_event_manager = TeamNominationEventManager(db)
        self.__participant_manager = ParticipantManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__event_manager = EventManager(db)
        self.__team_manager = TeamManager(db)
        self.__db = db

        self.__default_team_error = "default team is unchangeble"
        self.__participant_not_in_team_error = "participant not in team error"
        self.__participants_already_in_team_error = "participants already in team"
        self.__team_already_in_nomination_event_error = "team already in nomination event"
        self.__participant_in_another_team_error = "participant in another team"
        self.__participant_already_in_nomination_event = "participant already in nomination event"
        self.__registration_finished_error = "Registration_finished"

    def check_team_event_nomination__nomination_event__existence(self,
                                                                 team_name: str,
                                                                 nomination_name: str,
                                                                 event_name: str
                                                                 ):
        self.__team_manager.raise_exception_if_not_found(team_name)
        self.check_event_nomination__nomination_event_existence(nomination_name, event_name)

    def check_event_nomination__nomination_event_existence(self,
                                                           nomination_name: str,
                                                           event_name: str
                                                           ):
        self.__event_manager.raise_exception_if_not_found(event_name)
        self.__nomination_manager.raise_exception_if_not_found(nomination_name)
        self.__nomination_event_manager.raise_exception_if_not_found(nomination_name, event_name)

    def check_if_team_not_in_event_nomination(
            self,
            team_name,
            nomination_name,
            event_name
    ):
        self.__team_nomination_event_manager.raise_exception_if_team_not_in_event_nomination(
            team_name,
            nomination_name,
            event_name
        )

    def validate_user_entity_ownership(self, decoded_token: TokenDecodedSchema, team_name: str, event_name: str):
        if decoded_token.role == UserRole.specialist or decoded_token.role == UserRole.judge:
            self.__team_manager.raise_exception_if_owner_wrong(team_name, decoded_token.user_id)
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_owner_wrong(event_name, decoded_token.user_id)

    def check_participant_and_team_existence(self, participant_email: EmailStr, team_name: str):
        self.__participant_manager.raise_exception_if_not_found(participant_email)
        self.__team_manager.raise_exception_if_not_found(team_name)

    def raise_exception_if_team_default(self, team: TeamSchema):
        if "default_team" in team.name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__default_team_error}
            )

    def check_nomination_event__nomination_event_existence(self, nomination_name: str, event_name: str):
        self.__nomination_manager.raise_exception_if_not_found(nomination_name)
        self.__event_manager.raise_exception_if_not_found(event_name)
        self.__nomination_event_manager.raise_exception_if_not_found(nomination_name, event_name)

    def raise_exception_if_participants_not_in_team(self, team_name: str, participant_email: EmailStr):
        team_participants_emails = set(get_team_participants_emails_db(self.__db, team_name))
        if participant_email not in team_participants_emails:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_not_in_team_error}
            )

    def raise_exception_if_participant_in_nomination_event(self, participant_email: EmailStr, nomination_name: str, event_name: str):
        nomination_event_participant_emails = set(
            participant_db.email for participant_db in
            get_participants_of_nomination_event_db(self.__db, nomination_name, event_name)
        )

        if participant_email in nomination_event_participant_emails:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_already_in_nomination_event}
            )

    def raise_exception_if_registration_finished(self, nomination_name: str, event_name: str):
        nomination_event_db = get_nomination_event_db(self.__db, nomination_name, event_name)
        if nomination_event_db.registration_finished:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error", self.__registration_finished_error}
            )
