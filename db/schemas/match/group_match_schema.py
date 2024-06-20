from pydantic import BaseModel, EmailStr

from db.schemas.team.team_get import TeamGetSchema


class GroupMatchSchema(BaseModel):
    match_id: int
    team1: TeamGetSchema | None
    team2: TeamGetSchema | None
    winner: TeamGetSchema | None

    last_result_creator_email: EmailStr | None
    match_queue_number: int

    class Config:
        from_attributes = True
