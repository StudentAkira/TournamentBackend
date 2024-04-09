from starlette.responses import Response

from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema
from db.schemas.team.team import TeamSchema
from managers.event import EventManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.team import TeamManager
from managers.token import TokenManager
from managers.tournament import TournamentManager
from managers.user import UserManager
from utils.retriever_util import Retriever
from utils.validation_util import Validator


class TournamentService:

    def __init__(self, db):
        self.__db = db

        self.__event_manager = EventManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__token_manager = TokenManager(db)
        self.__tournament_manager = TournamentManager(db)
        self.__team_manager = TeamManager(db)
        self.__user_manager = UserManager(db)

        self.__validator = Validator(db)
        self.__retriever = Retriever(db)

        self.__groups_created_message = "groups are created"
        self.__group_stage_finished_message = "group stage finished"
        self.__play_off_tournament_started = "play off stage started"
        self.__play_off_stage_finished_message = "play off stage finished"

    def start_group_stage(
            self,
            response: Response,
            token: str,
            nomination_event: OlympycNominationEventSchema,
            group_count: int
    ):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event_check_judge_in_command(
                response,
                token,
                nomination_event
            )
        self.__nomination_event_manager.raise_exception_if_tournament_started(nomination_event_db)
        self.__tournament_manager.start_group_stage(nomination_event_db, group_count)
        return {"message": self.__groups_created_message}

    def get_groups_of_tournament(self, response: Response, token: str, nomination_event: OlympycNominationEventSchema):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event_check_judge_in_command(
                response, token, nomination_event
            )
        return self.__tournament_manager.get_groups_of_tournament(nomination_event_db)

    def finish_group_stage(self, response: Response, token: str, nomination_event: OlympycNominationEventSchema):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db =\
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event_check_judge_in_command(
                response,
                token,
                nomination_event
            )
        self.__tournament_manager.raise_exception_if_not_all_matches_finished(nomination_event_db)
        self.__tournament_manager.raise_exception_if_group_stage_finished(nomination_event_db)
        self.__nomination_event_manager.raise_exception_if_tournament_not_started(nomination_event_db)
        self.__tournament_manager.finish_group_stage(nomination_event_db)
        return {"message": self.__group_stage_finished_message}

    def start_play_off_tournament(
            self,
            response: Response,
            token: str,
            nomination_event: OlympycNominationEventSchema,
            teams: list[TeamSchema]
    ):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event_check_judge_in_command(
                response,
                token,
                nomination_event
            )
        teams = [TeamSchema(
            name=self.__team_manager.get_team_name_from_team_name_or_participant_email(team.name)
        ) for team in teams]

        self.__tournament_manager.raise_exception_if_teams_not_in_tournament(teams, nomination_event_db)
        self.__tournament_manager.raise_exception_if_group_stage_not_finished(nomination_event_db)
        self.__tournament_manager.raise_exception_if_play_off_stage_started(nomination_event_db)
        self.__tournament_manager.start_play_off_tournament(nomination_event_db, teams)
        return {"message": self.__play_off_tournament_started}

    def finish_play_off_stage(self, response: Response, token: str, nomination_event: OlympycNominationEventSchema):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event_check_judge_in_command(
                response,
                token,
                nomination_event
            )
        self.__tournament_manager.raise_exception_if_not_all_matches_finished(nomination_event_db)
        self.__nomination_event_manager.raise_exception_if_tournament_not_started(nomination_event_db)
        self.__tournament_manager.raise_exception_if_play_off_stage_finished(nomination_event_db)
        self.__tournament_manager.finish_play_off_stage(nomination_event_db)
        return {"message": self.__play_off_stage_finished_message}
