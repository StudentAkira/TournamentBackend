from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event.nomination_event import NominationEventSchema
from db.schemas.nomination_event.nomination_event_type import NominationEventType
from db.schemas.nomination_event.time_nomination_event import TimeNominationEventSchema
from db.schemas.race_round.race_round_create import RaceRoundCreateSchema
from db.schemas.race_round.race_round_update import RaceRoundUpdateSchema
from managers.nomination_event import NominationEventManager
from managers.participant import ParticipantManager
from managers.race_round import RaceRoundManager
from managers.team import TeamManager
from managers.team_nomination_event import TeamNominationEventManager
from managers.team_participant import TeamParticipantManager
from managers.token import TokenManager
from utils.retriever_util import Retriever


class RaceRoundService:

    def __init__(self, db: Session):
        self.__db = db

        self.__retriever = Retriever(db)
        self.__race_round_manager = RaceRoundManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__team_manager = TeamManager(db)
        self.__team_nomination_event_manager = TeamNominationEventManager(db)
        self.__team_participant_manager = TeamParticipantManager(db)
        self.__participant_manager = ParticipantManager(db)

        self.__race_round_result_set_message = "Race round result set"

    def get_race_rounds(
            self,
            response: Response,
            token: str,
            event_name: str,
            nomination_name: str
    ):
        nomination_event = NominationEventSchema(
            event_name=event_name,
            nomination_name=nomination_name,
            type=NominationEventType.time
        )
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event(
                response,
                token,
                nomination_event
            )
        self.__nomination_event_manager.raise_exception_if_user_not_in_judge_command(
            nomination_event_db,
            user_db
        )
        return self.__race_round_manager.get_race_rounds(nomination_event_db)

    def set_race_rounds(self, response: Response, token: str, race_round: RaceRoundCreateSchema):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.__retriever.get_decoded_token_user_nomination_event_nomination_event(
                response,
                token,
                race_round.nomination_event.to_nomination_event_schema()
            )
        self.__nomination_event_manager.raise_exception_if_user_not_in_judge_command(
            nomination_event_db,
            user_db
        )

        team_name = self.__team_manager.get_team_name_from_team_name_or_participant_email(race_round.team_name)
        team_db = self.__team_manager.get_by_name_or_raise_if_not_found(team_name)

        self.__team_nomination_event_manager.raise_exception_if_team_not_in_event_nomination(
            team_db,
            nomination_event_db
        )

        self.__race_round_manager.raise_exception_if_round_overlast(nomination_event_db, team_db)
        self.__race_round_manager.set_race_rounds(nomination_event_db, team_db, race_round.result)
        return {"message": self.__race_round_result_set_message}

    def update_race_rounds(self, response: Response, token: str, race_round: RaceRoundUpdateSchema):
        pass
