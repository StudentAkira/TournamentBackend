from pydantic import BaseModel, Field, EmailStr, validator

from db.schemas.nomination_event import NominationEventSchema, OlympycNominationEventSchema
from db.schemas.team import TeamSchema
from db.schemas.team_participant import TeamParticipantsSchema


class MatchSchema(BaseModel):
    match_id: int
    team1: TeamSchema | None
    team2: TeamSchema | None
    winner: TeamSchema | None

    last_result_creator_email: EmailStr | None
    match_queue_number: int

    class Config:
        from_attributes = True


class SetMatchResultSchema(BaseModel):
    nomination_event: OlympycNominationEventSchema

    match_id: int
    winner_team_name: str | None = None

    @validator('winner_team_name')
    def validate_winner_team_name(cls, value: str | None):
        if value is None:
            return value
        if len(value) <= 3:
            raise ValueError(f"team name should be at least 3 characters length, {value}")
        return value
