from pydantic import EmailStr
from starlette.responses import Response

from db.schemas.nomination_event import NominationEventSchema, NominationEventNameSchema
from db.schemas.team import TeamSchema
from db.schemas.user import UserRole
from managers.event_manager import EventManager
from managers.nomination_event_manager import NominationEventManager
from managers.nomination_manager import NominationManager
from managers.paticipant_manager import ParticipantManager
from managers.team_manager import TeamManager
from managers.token_manager import TokenManager
from validators.validator import Validator


class TournamentRegistrationService:
    def __init__(self, db):
        self.__db = db

        self.__event_manager = EventManager(db)
        self.__token_manager = TokenManager(db)
        self.__team_manager = TeamManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__participant_manager = ParticipantManager(db)

        self.__validator = Validator(db)

        self.__team_appended_message = "team appended to nomination event"

    def get_teams_of_nomination_event(
            self,
            response: Response,
            token: str,
            nomination_name: str,
            event_name: str,
    ) -> list[TeamSchema]:
        decoded_token = self.__token_manager.decode_token(token, response)

        self.__validator.check_event_nomination__nomination_event_existence(nomination_name, event_name)
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_event_owner_wrong(event_name, decoded_token.user_id)

        return self.__nomination_event_manager.get_teams_of_nomination_event(nomination_name, event_name)

    def append_team_to_event_nomination(
            self,
            response: Response,
            token: str,
            team_name_or_participant_email: str,
            participant_emails: list[EmailStr],
            nomination_name: str,
            event_name: str,
    ):

        team_name = self.get_team_name_from_team_name_or_participant_email(team_name_or_participant_email)

        decoded_token = self.__token_manager.decode_token(token, response)

        self.__validator.check_team_event_nomination__nomination_event__existence(team_name, nomination_name,
                                                                                  event_name)
        self.__validator.validate_user_entity_ownership(decoded_token, team_name, event_name)
        self.__validator.raise_exception_if_participants_in_team(team_name, participant_emails)
        self.__validator.raise_exception_if_team_already_in_nomination_event(team_name, nomination_name, event_name)

        self.__validator.raise_exception_if_participant_in_another_team(team_name, nomination_name, event_name)

        self.__nomination_event_manager.append_team_to_event_nomination(
            team_name,
            participant_emails,
            nomination_name,
            event_name
        )

        return {"message": self.__team_appended_message}

    def get_team_name_from_team_name_or_participant_email(self, team_name_or_participant_email):
        return self.__team_manager.get_team_name_from_team_name_or_participant_email(team_name_or_participant_email)

    def get_nomination_events_full_info(
            self,
            response: Response,
            token: str,
            offset: int,
            limit: int
    ) -> list[NominationEventSchema]:
        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role != UserRole.judge:
            return self.__nomination_event_manager.get_nominations_events_full_info(offset, limit)
        return self.__nomination_event_manager.get_nominations_events_full_info_by_owner(
            offset,
            limit,
            decoded_token.user_id
        )

    def get_nomination_events_names(
            self,
            response: Response,
            token: str,
            offset: int,
            limit: int
    ) -> list[NominationEventNameSchema]:
        decoded_token = self.__token_manager.decode_token(token, response)
        if decoded_token.role != UserRole.judge:
            return self.__nomination_event_manager.get_nominations_events_names(offset, limit)
        return self.__nomination_event_manager.get_nominations_events_names_by_owner(
            offset,
            limit,
            decoded_token.user_id
        )
