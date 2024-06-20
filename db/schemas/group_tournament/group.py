from pydantic import BaseModel

from db.schemas.team.team_get import TeamGetSchema


class GroupSchema(BaseModel):
    id: int

    teams: list[TeamGetSchema]

    class Config:
        from_attributes = True
