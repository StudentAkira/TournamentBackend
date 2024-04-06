from pydantic import BaseModel, Field

from db.schemas.match import GroupMatchSchema
from db.schemas.nomination_event import OlympycNominationEventSchema
from db.schemas.team import TeamSchema


class GroupSchema(BaseModel):
    id: int

    teams: list[TeamSchema]

    class Config:
        from_attributes = True


class StartGroupTournamentSchema(BaseModel):
    olympyc_nomination_event: OlympycNominationEventSchema

    group_count: int = Field(gt=0)


class GetGroupsOfTournamentSchema(BaseModel):
    groups: list[GroupSchema]

    class Config:
        from_attributes = True


class GroupMatchesSchema(BaseModel):
    group_id: int

    matches: list[GroupMatchSchema]

    class Config:
        from_attributes = True
