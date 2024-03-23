from pydantic import BaseModel

from db.schemas.team import TeamSchema
from db.schemas.team_participant import TeamParticipantsSchema


class MatchSchema(BaseModel):
    match_id: int
    team1: TeamSchema | None
    team2: TeamSchema | None
    winner: TeamSchema | None

    match_queue_number: int

    class Config:
        from_attributes = True
