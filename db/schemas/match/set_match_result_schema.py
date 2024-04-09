from pydantic import BaseModel, validator, field_validator

from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema


class SetMatchResultSchema(BaseModel):
    nomination_event: OlympycNominationEventSchema

    match_id: int
    winner_team_name: str | None

    @field_validator('winner_team_name')
    def validate_winner_team_name(cls, value: str | None):
        if value is None:
            return value
        if len(value) <= 3:
            raise ValueError(f"team name should be at least 3 characters length, {value}")
        return value
