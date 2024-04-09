from pydantic import field_validator

from db.schemas.race_round.race_round import RaceRoundSchema


class RaceRoundUpdateSchema(RaceRoundSchema):
    team_id: int
    result: float

    @field_validator("result")
    def validate(cls, value):
        if value < 0:
            raise ValueError("Value must positive")
        return value
