from pydantic import BaseModel, validator, field_validator

from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema


class SetGroupMatchResultSchema(BaseModel):
    nomination_event: OlympycNominationEventSchema

    match_id: int
    team1_score: int
    team2_score: int
