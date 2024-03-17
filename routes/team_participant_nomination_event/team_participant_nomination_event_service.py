from starlette.responses import Response

from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.schemas.team_nomination_event import AppendTeamParticipantNominationEventSchema, \
    DeleteTeamParticipantNominationEventSchema
from managers.event import EventManager
from managers.nomination_event import NominationEventManager
from managers.nomination import NominationManager
from managers.participant import ParticipantManager
from managers.team import TeamManager
from managers.team_participant_nomination_event import TeamParticipantNominationEventManager
from managers.token import TokenManager
from validators.validator import Validator


class TeamParticipantNominationEventService:
    def __init__(self, db):
        self.__db = db

        self.__event_manager = EventManager(db)
        self.__token_manager = TokenManager(db)
        self.__team_manager = TeamManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__participant_manager = ParticipantManager(db)
        self.__team_participant_nomination_event_manager = TeamParticipantNominationEventManager(db)

        self.__validator = Validator(db)

        self.__team_participant_appended_message = "team participant appended to nomination event"
        self.__team_participant_deleted_message = "team participant deleted from nomination event"

    def append_team_participant_nomination_event(
            self,
            response: Response,
            token: str,
            team_participant_nomination_event_data: AppendTeamParticipantNominationEventSchema
    ):
        team_name = self.get_team_name_from_team_name_or_participant_email(
            team_participant_nomination_event_data.team_name
        )
        team_participant_nomination_event_data.team_name = team_name
        self.team_participant_nomination_event_validations(response, token, team_participant_nomination_event_data)
        self.__team_participant_nomination_event_manager.append_team_participant_nomination_event(
            team_participant_nomination_event_data
        )
        return {"message": self.__team_participant_appended_message}

    def delete_team_participant_nomination_event(
            self,
            response: Response,
            token: str,
            team_participant_nomination_event_data: DeleteTeamParticipantNominationEventSchema
    ):
        team_name = self.get_team_name_from_team_name_or_participant_email(
            team_participant_nomination_event_data.team_name
        )
        team_participant_nomination_event_data.team_name = team_name
        self.team_participant_nomination_event_validations(response, token, team_participant_nomination_event_data)
        self.__team_participant_nomination_event_manager.delete_team_participant_nomination_event(
            team_participant_nomination_event_data
        )
        return {"message": self.__team_participant_deleted_message}

    def get_team_name_from_team_name_or_participant_email(self, team_name_or_participant_email):
        return self.__team_manager.get_team_name_from_team_name_or_participant_email(team_name_or_participant_email)

    def team_participant_nomination_event_validations(
            self,
            response: Response,
            token: str,
            team_participant_nomination_event_data
        ):
        decoded_token = self.__token_manager.decode_token(token, response)
        team_name = team_participant_nomination_event_data.team_name
        nomination_name = team_participant_nomination_event_data.nomination_name
        event_name = team_participant_nomination_event_data.event_name
        participant_email = team_participant_nomination_event_data.participant_email
        self.__validator.raise_exception_if_registration_finished(nomination_name, event_name)
        self.__team_manager.raise_exception_if_not_found(team_name)
        self.__participant_manager.raise_exception_if_not_found(participant_email)
        self.__nomination_event_manager.raise_exception_if_not_found(nomination_name, event_name)
        self.__validator.validate_user_entity_ownership(decoded_token, team_name, event_name)
        self.__validator.raise_exception_if_participants_not_in_team(team_name, participant_email)
        self.__validator.raise_exception_if_participant_in_nomination_event(
            participant_email,
            nomination_name,
            event_name
        )
