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
from managers.team_participant import TeamParticipantManager
from managers.team_participant_nomination_event import TeamParticipantNominationEventManager
from managers.token import TokenManager
from managers.user import UserManager
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
        self.__team_participant_manager = TeamParticipantManager(db)
        self.__user_manager = UserManager(db)

        self.__validator = Validator(db)

        self.__team_participant_appended_message = "team participant appended to nomination event"
        self.__team_participant_updated_message = "team participant updated in nomination event"
        self.__team_participant_deleted_message = "team participant deleted from nomination event"

    def append_team_participant_nomination_event(
            self,
            response: Response,
            token: str,
            team_participant_nomination_event: AppendTeamParticipantNominationEventSchema
    ):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db, participant_db = \
            self.get_decoded_token_user_event_nomination_nomination_event_participant(
                response,
                token,
                team_participant_nomination_event
            )
        team_name = self.__team_manager.get_team_name_from_team_name_or_participant_email(
            team_participant_nomination_event.team_name
        )
        team_participant_nomination_event.team_name = team_name
        team_db = self.__team_manager.get_by_name_or_raise_if_not_found(team_name)
        self.__team_participant_manager.raise_exception_if_participant_not_in_team(
            participant_db,
            team_db
        )
        self.__validator.validate_user_entity_ownership(
            decoded_token,
            team_db,
            event_db
        )
        self.__nomination_event_manager.raise_exception_if_registration_finished(nomination_event_db)
        self.__nomination_event_manager.raise_exception_if_participant_in_nomination_event(
            participant_db, nomination_event_db
        )
        self.__participant_manager.raise_exception_if_owner_wrong(
            participant_db,
            user_db
        )
        self.__team_participant_nomination_event_manager.append_team_participant_nomination_event(
            nomination_event_db,
            team_db,
            participant_db,
            team_participant_nomination_event
        )
        return {"message": self.__team_participant_appended_message}

    def update_team_participant_nomination_event(
            self,
            response: Response,
            token: str,
            team_participant_nomination_event: UpdateTeamParticipantNominationEventSchema
    ):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db, participant_db = \
            self.get_decoded_token_user_event_nomination_nomination_event_participant(
                response,
                token,
                team_participant_nomination_event
            )

        self.__nomination_event_manager.raise_exception_if_participant_not_in_nomination_event(
            participant_db.email,
            nomination_event_db
        )
        self.__nomination_event_manager.raise_exception_if_registration_finished(nomination_event_db)
        self.__participant_manager.raise_exception_if_owner_wrong(
            participant_db,
            user_db
        )
        self.__team_participant_nomination_event_manager.update_team_participant_nomination_event(
            nomination_event_db,
            participant_db,
            team_participant_nomination_event
        )
        return {"message": self.__team_participant_updated_message}

    def delete_team_participant_nomination_event(
            self,
            response: Response,
            token: str,
            team_participant_nomination_event: DeleteTeamParticipantNominationEventSchema
    ):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db, participant_db = \
            self.get_decoded_token_user_event_nomination_nomination_event_participant(
                response,
                token,
                team_participant_nomination_event
            )
        self.__event_manager.raise_exception_if_owner_wrong(
            event_db,
            decoded_token.user_id
        )
        self.__participant_manager.raise_exception_if_owner_wrong(
            participant_db,
            user_db
        )
        self.__nomination_event_manager.raise_exception_if_registration_finished(nomination_event_db)
        self.__nomination_event_manager.raise_exception_if_participant_not_in_nomination_event(
            participant_db.email,
            nomination_event_db
        )
        self.__team_participant_nomination_event_manager.delete_team_participant_nomination_event(
            nomination_event_db, participant_db
        )
        return {"message": self.__team_participant_deleted_message}

    def get_decoded_token_user_event_nomination_nomination_event_participant(
            self,
            response: Response,
            token: str,
            team_participant_nomination_event:
            DeleteTeamParticipantNominationEventSchema |
            UpdateTeamParticipantNominationEventSchema |
            AppendTeamParticipantNominationEventSchema
    ):

        decoded_token = self.__token_manager.decode_token(token, response)
        user_db = self.__user_manager.get_user_by_id_or_raise_if_not_found(decoded_token.user_id)
        event_db = self.__event_manager.get_by_name_or_raise_if_not_found(
            team_participant_nomination_event.event_name
        )
        nomination_db = self.__nomination_manager.get_by_name_or_raise_exception_if_not_found(
            team_participant_nomination_event.nomination_name
        )
        nomination_event_db = self.__nomination_event_manager.get_nomination_event_or_raise_if_not_found(
            nomination_db,
            event_db,
            team_participant_nomination_event.nomination_event_type
        )
        participant_db = self.__participant_manager.get_by_email_or_raise_if_not_found(
            team_participant_nomination_event.participant_email
        )
        return decoded_token, user_db, event_db, nomination_db, nomination_event_db, participant_db
