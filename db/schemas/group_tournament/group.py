from pydantic import BaseModel

from db.schemas.team.team import TeamSchema


class GroupSchema(BaseModel):
    id: int

    teams: list[TeamSchema]

    class Config:
        from_attributes = True
