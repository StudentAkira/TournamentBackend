from pydantic import BaseModel

from db.schemas.match.group_match_schema import GroupMatchSchema


class GroupMatchesSchema(BaseModel):
    group_id: int

    matches: list[GroupMatchSchema]

    class Config:
        from_attributes = True