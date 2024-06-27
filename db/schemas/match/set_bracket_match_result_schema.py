from pydantic import BaseModel

from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema


class SetBracketMatchResultSchema(BaseModel):
    nomination_event: OlympycNominationEventSchema

    match_id: int
    team1_score: int
    team2_score: int