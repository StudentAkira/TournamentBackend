from pydantic import BaseModel, Field, EmailStr

from db.schemas.nomination_event import NominationEventSchema
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
    nomination_event: NominationEventSchema

    match_id: int
    winner_team_name: str = Field(min_length=3)
