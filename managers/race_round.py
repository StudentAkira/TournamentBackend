from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from db.crud.race_round.race_round import get_race_rounds_db, set_race_round_result_db
from db.models.nomination_event import NominationEvent
from db.models.team import Team
from db.schemas.race_round.race_roun_result import RaceRoundResultSchema
from db.schemas.race_round.race_round_update import RaceRoundUpdateSchema


class RaceRoundManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__too_many_rounds_error = "too many rounds"

    def get_race_rounds(
            self,
            nomination_event_db: type(NominationEvent)
    ):
        race_rounds_db = get_race_rounds_db(nomination_event_db)
        race_rounds = [
            RaceRoundResultSchema(team_name=race_round_db.team.name, result=race_round_db.result)
            for race_round_db in race_rounds_db
        ]
        return race_rounds

    def set_race_rounds(
            self,
            nomination_event_db: type(NominationEvent),
            team_db: type(Team),
            result: float
    ):
        set_race_round_result_db(self.__db, nomination_event_db, team_db, result)

    def update_race_rounds(self, response: Response, token: str, race_round: RaceRoundUpdateSchema):
        pass

    def raise_exception_if_round_overlast(self, nomination_event_db: type(NominationEvent), team_db: type(Team)):
        race_rounds_of_nomination_event_with_team = [
            race_round_db
            for race_round_db in nomination_event_db.race_rounds
            if race_round_db.team == team_db
        ]
        print(nomination_event_db.race_rounds)
        if len(race_rounds_of_nomination_event_with_team) == nomination_event_db.race_round_length:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__too_many_rounds_error}
            )
