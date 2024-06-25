from pydantic import BaseModel, EmailStr

from db.schemas.team.team_get import TeamGetSchema


class BracketMatchSchema(BaseModel):
    match_id: int
    team1: TeamGetSchema | None
    team2: TeamGetSchema | None
    winner: TeamGetSchema | None

    last_result_creator_email: EmailStr | None
    next_match_id: int | None

    class Config:
        from_attributes = True