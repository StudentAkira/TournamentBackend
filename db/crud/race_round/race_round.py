from sqlalchemy.orm import Session

from db.models.nomination_event import NominationEvent
from db.models.participant import Participant
from db.models.race_round import RaceRound


def get_race_rounds_db(nomination_event_db: type(NominationEvent)):
    return nomination_event_db.race_rounds


def set_race_round_result_db(
        db: Session,
        nomination_event_db: type(NominationEvent),
        team_db: type(Participant),
        result: float
):
    if not nomination_event_db.tournament_started:
        nomination_event_db.tournament_started = True
    race_round = RaceRound(
        result=result
    )
    race_round.team = team_db
    race_round.nomination_event = nomination_event_db

    team_db.race_rounds.append(race_round)
    nomination_event_db.race_rounds.append(race_round)
    db.add(race_round)
    db.add(team_db)
    db.add(nomination_event_db)
    db.commit()
