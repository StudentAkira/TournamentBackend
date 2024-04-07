from pydantic import BaseModel

from db.schemas.group_tournament.group import GroupSchema


class GetGroupsOfTournamentSchema(BaseModel):
    groups: list[GroupSchema]

    class Config:
        from_attributes = True