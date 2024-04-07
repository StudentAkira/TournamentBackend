from starlette.responses import Response

from db.schemas.team_nomination_event.append_team_participant_nomination_event import \
    AppendTeamParticipantNominationEventSchema
from db.schemas.team_nomination_event.delete_team_participant_nomination_event import \
    DeleteTeamParticipantNominationEventSchema
from db.schemas.team_nomination_event.update_team_participant_nomination_event import \
    UpdateTeamParticipantNominationEventSchema
from managers.event import EventManager
from managers.nomination_event import NominationEventManager
from managers.nomination import NominationManager
from managers.participant import ParticipantManager
from managers.team import TeamManager
from managers.team_participant_nomination_event import TeamParticipantNominationEventManager
from managers.token import TokenManager
from utils.validation_util import Validator


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
        self.__team_participant_updated_message = "team participant updated in nomination event"
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
        decoded_token = self.__token_manager.decode_token(token, response)

        self.__event_manager.raise_exception_if_not_found(
            team_participant_nomination_event_data.event_name
        )
        self.__nomination_manager.raise_exception_if_not_found(
            team_participant_nomination_event_data.nomination_name
        )
        self.__team_manager.raise_exception_if_not_found(
            team_participant_nomination_event_data.team_name
        )
        self.__participant_manager.raise_exception_if_not_found(
            team_participant_nomination_event_data.participant_email
        )
        self.__nomination_event_manager.raise_exception_if_not_found(
            team_participant_nomination_event_data.nomination_name,
            team_participant_nomination_event_data.event_name,
            team_participant_nomination_event_data.nomination_event_type
        )
        self.__validator.raise_exception_if_participant_not_in_team(
            team_name,
            team_participant_nomination_event_data.participant_email
        )
        self.__validator.validate_user_entity_ownership(
            decoded_token,
            team_name,
            team_participant_nomination_event_data.event_name
        )

        self.__validator.raise_exception_if_registration_finished(
            team_participant_nomination_event_data.nomination_name,
            team_participant_nomination_event_data.event_name,
            team_participant_nomination_event_data.nomination_event_type
        )

        self.__validator.raise_exception_if_participant_in_nomination_event(
            team_participant_nomination_event_data.participant_email,
            team_participant_nomination_event_data.nomination_name,
            team_participant_nomination_event_data.event_name,
            team_participant_nomination_event_data.nomination_event_type
        )

        self.__participant_manager.raise_exception_if_owner_wrong(##may be changed
            team_participant_nomination_event_data.participant_email,
            decoded_token.user_id
        )

        self.__team_participant_nomination_event_manager.append_team_participant_nomination_event(
            team_participant_nomination_event_data
        )
        return {"message": self.__team_participant_appended_message}

    def update_team_participant_nomination_event(
            self,
            response: Response,
            token: str,
            team_participant_nomination_event_data: UpdateTeamParticipantNominationEventSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)

        self.__participant_manager.raise_exception_if_not_found(
            team_participant_nomination_event_data.participant_email
        )

        self.__event_manager.raise_exception_if_not_found(team_participant_nomination_event_data.event_name)
        self.__nomination_manager.raise_exception_if_not_found(team_participant_nomination_event_data.nomination_name)
        self.__nomination_event_manager.raise_exception_if_not_found(
            team_participant_nomination_event_data.nomination_name,
            team_participant_nomination_event_data.event_name,
            team_participant_nomination_event_data.nomination_event_type
        )
        self.__validator.raise_exception_if_participant_not_in_nomination_event(
            team_participant_nomination_event_data.participant_email,
            team_participant_nomination_event_data.nomination_name,
            team_participant_nomination_event_data.event_name,
            team_participant_nomination_event_data.nomination_event_type
        )

        self.__validator.raise_exception_if_registration_finished(
            team_participant_nomination_event_data.nomination_name,
            team_participant_nomination_event_data.event_name,
            team_participant_nomination_event_data.nomination_event_type
        )

        self.__event_manager.raise_exception_if_owner_wrong(
            team_participant_nomination_event_data.event_name,
            decoded_token.user_id
        )
        self.__participant_manager.raise_exception_if_owner_wrong(
            team_participant_nomination_event_data.participant_email,
            decoded_token.user_id
        )

        self.__team_participant_nomination_event_manager.update_team_participant_nomination_event(
            team_participant_nomination_event_data
        )
        return {"message": self.__team_participant_updated_message}

    def delete_team_participant_nomination_event(
            self,
            response: Response,
            token: str,
            team_participant_nomination_event_data: DeleteTeamParticipantNominationEventSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)

        self.__participant_manager.raise_exception_if_not_found(
            team_participant_nomination_event_data.participant_email
        )

        self.__event_manager.raise_exception_if_not_found(team_participant_nomination_event_data.event_name)
        self.__nomination_manager.raise_exception_if_not_found(team_participant_nomination_event_data.nomination_name)
        self.__nomination_event_manager.raise_exception_if_not_found(
            team_participant_nomination_event_data.nomination_name,
            team_participant_nomination_event_data.event_name,
            team_participant_nomination_event_data.nomination_event_type
        )
        self.__validator.raise_exception_if_participant_not_in_nomination_event(
            team_participant_nomination_event_data.participant_email,
            team_participant_nomination_event_data.nomination_name,
            team_participant_nomination_event_data.event_name,
            team_participant_nomination_event_data.nomination_event_type
        )

        self.__event_manager.raise_exception_if_owner_wrong(
            team_participant_nomination_event_data.event_name,
            decoded_token.user_id
        )
        self.__participant_manager.raise_exception_if_owner_wrong(
            team_participant_nomination_event_data.participant_email,
            decoded_token.user_id
        )

        self.__validator.raise_exception_if_registration_finished(
            team_participant_nomination_event_data.nomination_name,
            team_participant_nomination_event_data.event_name,
            team_participant_nomination_event_data.nomination_event_type
        )

        self.__team_participant_nomination_event_manager.delete_team_participant_nomination_event(
            team_participant_nomination_event_data
        )
        return {"message": self.__team_participant_deleted_message}

    def get_team_name_from_team_name_or_participant_email(self, team_name_or_participant_email):
        return self.__team_manager.get_team_name_from_team_name_or_participant_email(team_name_or_participant_email)
