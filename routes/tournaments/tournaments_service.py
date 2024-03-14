from starlette.responses import Response

from db.schemas.nomination_event import NominationEventSchema
from managers.nomination_event import NominationEventManager
from managers.token import TokenManager


class TournamentService:

    def __init__(self, db):
        self.__db = db

        self.__nomination_event_manager = NominationEventManager(db)
        self.__token_manager = TokenManager(db)

    def start_group_tournament(self, response: Response, token: str, nomination_event: NominationEventSchema):
        #
        # decoded_token = self.__token_manager.decode_token(token, response)
        #
        # teams = self.__nomination_event_manager.get_teams_of_nomination_event(
        #     nomination_event.nomination_name, nomination_event.event_name
        # )
        # self.__nomination_event_manager.finish_event_nomination_registration(
        #     nomination_event.nomination_name, nomination_event.event_name
        # )
        # return teams
        pass
