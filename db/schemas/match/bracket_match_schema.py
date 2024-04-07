from pydantic import BaseModel, EmailStr

from db.schemas.team.team import TeamSchema


class BracketMatchSchema(BaseModel):
    match_id: int
    team1: TeamSchema | None
    team2: TeamSchema | None
    winner: TeamSchema | None

    last_result_creator_email: EmailStr | None
    next_match_id: int | None

    class Config:
        from_attributes = True