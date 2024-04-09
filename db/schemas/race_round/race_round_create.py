from pydantic import field_validator, Field, EmailStr

from db.schemas.race_round.race_round import RaceRoundSchema


class RaceRoundCreateSchema(RaceRoundSchema):
    team_name: str = Field(min_length=3)
    result: float

    @field_validator("result")
    def validate(cls, value):
        if value < 0:
            raise ValueError("Value must positive")
        return value
