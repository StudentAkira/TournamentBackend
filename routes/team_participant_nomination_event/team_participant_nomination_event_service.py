from starlette.responses import Response

from db.schemas.team_nomination_event.delete_team_participant_nomination_event import \
    DeleteTeamParticipantNominationEventSchema
from db.schemas.team_nomination_event.update_team_participant_nomination_event import \
    UpdateTeamParticipantNominationEventSchema
from db.schemas.team_participant_nomination_event.append_teams_participants_nomination_event import \
    TeamParticipantNominationEventAppendSchema
from managers.event import EventManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.participant import ParticipantManager
from managers.team import TeamManager
from managers.team_participant import TeamParticipantManager
from managers.team_participant_nomination_event import TeamParticipantNominationEventManager
from managers.token import TokenManager
from managers.user import UserManager
from utils.retriever_util import Retriever
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
        self.__retriever = Retriever(db)

        self.__team_participant_appended_message = "team participants appended to nomination event"
        self.__team_participant_updated_message = "team participant updated in nomination event"
        self.__team_participant_deleted_message = "team participant deleted from nomination event"

    def append_team_participant_nomination_event(
            self,
            response: Response,
            token: str,
            team_participant_nomination_event: TeamParticipantNominationEventAppendSchema
    ):

        event_db = self.__event_manager.get_by_id_or_raise_if_not_found(
            team_participant_nomination_event.nomination_event.event_id
        )
        nomination_db = self.__nomination_manager.get_by_id(
            team_participant_nomination_event.nomination_event.nomination_id
        )
        nomination_event_db = self.__nomination_event_manager.get_nomination_event_or_raise_if_not_found(
            nomination_db,
            event_db,
            team_participant_nomination_event.nomination_event.type
        )
        decoded_token = self.__token_manager.decode_token(token, response)
        user_db = self.__user_manager.get_user_by_id_or_raise_if_not_found(decoded_token.user_id)

        self.__team_participant_nomination_event_manager.validate_received_schema(
            team_participant_nomination_event,
            nomination_event_db,
            user_db
        )
        self.__team_participant_nomination_event_manager.refresh(team_participant_nomination_event, nomination_event_db)
        return {'message': self.__team_participant_appended_message}

    def update_team_participant_nomination_event(
            self,
            response: Response,
            token: str,
            team_participant_nomination_event: UpdateTeamParticipantNominationEventSchema
    ):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event(
                response,
                token,
                team_participant_nomination_event.to_nomination_event_schema()
            )
        participant_db = self.__participant_manager.get_by_email_or_raise_if_not_found(
            team_participant_nomination_event.participant_email
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
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event(
                response,
                token,
                team_participant_nomination_event.to_nomination_event_schema()
            )
        self.__event_manager.raise_exception_if_owner_wrong(
            event_db,
            decoded_token.user_id
        )
        participant_db = self.__participant_manager.get_by_email_or_raise_if_not_found(
            team_participant_nomination_event.participant_email
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
