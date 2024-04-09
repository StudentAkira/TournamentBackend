from pydantic import field_validator, Field, BaseModel


class RaceRoundResultSchema(BaseModel):
    team_name: str = Field(min_length=3)
    result: float

    @field_validator("result")
    def validate(cls, value):
        if value < 0:
            raise ValueError("Value must positive")
        return value

    class Config:
        from_attributes = True
