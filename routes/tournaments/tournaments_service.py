from starlette.responses import Response

from db.crud.tournaments import is_top_count_wrong_db
from db.schemas.group_tournament import StartGroupTournamentSchema
from db.schemas.nomination_event import NominationEventSchema
from managers.event import EventManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.token import TokenManager
from managers.tournament import TournamentManager


class TournamentService:

    def __init__(self, db):
        self.__db = db

        self.__event_manager = EventManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__token_manager = TokenManager(db)
        self.__tournament_manager = TournamentManager(db)

        self.__groups_created_message = "groups are created"
        self.__group_stage_finished_message = "group stage finished"
        self.__play_off_tournament_started = "play_off tournament started"

    def create_group_tournament(self, response: Response, token: str, nomination_event: StartGroupTournamentSchema):
        self.actions_validation(response, token, nomination_event)

        self.__nomination_event_manager.raise_exception_if_tournament_started(
            nomination_event.nomination_name,
            nomination_event.event_name,
            nomination_event.type
        )
        self.__tournament_manager.create_group_tournament(nomination_event)
        return {"message": self.__groups_created_message}

    def get_groups_of_tournament(self, response: Response, token: str, nomination_event: NominationEventSchema):
        self.actions_validation(response, token, nomination_event)
        return self.__tournament_manager.get_groups_of_tournament(nomination_event)

    def finish_group_stage(self, response: Response, token: str, nomination_event: NominationEventSchema):
        self.actions_validation(response, token, nomination_event)
        self.__tournament_manager.raise_exception_if_not_all_matches_finished(nomination_event)
        self.__tournament_manager.finish_group_stage(nomination_event)
        return {"message": self.__group_stage_finished_message}

    def start_play_off_tournament(
            self,
            response: Response,
            token: str,
            nomination_event: NominationEventSchema,
            top_count: int
    ):
        self.actions_validation(response, token, nomination_event)
        self.__tournament_manager.raise_exception_if_group_stage_not_finished(nomination_event)
        self.__tournament_manager.raise_exception_if_top_count_wrong(nomination_event, top_count)
        self.__tournament_manager.start_play_off_tournament(nomination_event, top_count)
        return {"message": self.__play_off_tournament_started}

    def actions_validation(
            self,
            response: Response,
            token: str,
            nomination_event:
                NominationEventSchema | StartGroupTournamentSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__nomination_manager.raise_exception_if_not_found(nomination_event.nomination_name)
        self.__event_manager.raise_exception_if_not_found(nomination_event.event_name)
        self.__nomination_event_manager.raise_exception_if_not_found(
            nomination_event.nomination_name,
            nomination_event.event_name,
            nomination_event.type
        )

        self.__event_manager.raise_exception_if_user_not_in_judge_command(
            nomination_event.nomination_name,
            nomination_event.event_name,
            nomination_event.type,
            decoded_token.user_id
        )
        self.__nomination_event_manager.raise_exception_if_nomination_event_not_olympyc(nomination_event.type)

