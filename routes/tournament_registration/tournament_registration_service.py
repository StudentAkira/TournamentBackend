from starlette.responses import Response
from db.schemas.team_nomination_event import AppendTeamToEventNominationSchema
from managers.event import EventManager
from managers.nomination_event import NominationEventManager
from managers.nomination import NominationManager
from managers.participant import ParticipantManager
from managers.team import TeamManager
from managers.team_nomination_event import TeamNominationEventManager
from managers.token import TokenManager
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
        self.__team_nomination_event_manager = TeamNominationEventManager(db)

        self.__validator = Validator(db)

        self.__team_appended_message = "team appended to nomination event"

    def append_team_to_event_nomination(
            self,
            response: Response,
            token: str,
            team_nomination_event_data: AppendTeamToEventNominationSchema
    ):

        team_name = self.get_team_name_from_team_name_or_participant_email(
            team_nomination_event_data.team_name
        )
        decoded_token = self.__token_manager.decode_token(token, response)

        team_nomination_event_data.team_name = team_name
        nomination_name = team_nomination_event_data.nomination_name
        event_name = team_nomination_event_data.event_name
        participant_emails = team_nomination_event_data.participant_emails

        self.__validator.check_team_event_nomination__nomination_event__existence(team_name, nomination_name,
                                                                                  event_name)
        self.__validator.validate_user_entity_ownership(decoded_token, team_name, event_name)
        self.__validator.raise_exception_if_participants_not_in_team(team_name, participant_emails)
        self.__validator.raise_exception_if_team_already_in_nomination_event(team_name, nomination_name, event_name)

        self.__validator.raise_exception_if_participant_in_another_team(team_name, nomination_name, event_name)

        self.__team_nomination_event_manager.append_team_to_nomination_event(
            team_nomination_event_data
        )

        return {"message": self.__team_appended_message}

    def get_team_name_from_team_name_or_participant_email(self, team_name_or_participant_email):
        return self.__team_manager.get_team_name_from_team_name_or_participant_email(team_name_or_participant_email)
