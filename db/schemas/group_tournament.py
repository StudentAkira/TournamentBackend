from pydantic import BaseModel, Field

from db.schemas.nomination_event import NominationEventType
from db.schemas.team import TeamSchema
from db.schemas.team_participant import TeamParticipantsSchema


class GroupSchema(BaseModel):
    id: int

    teams: list[TeamParticipantsSchema]

    class Config:
        from_attributes = True


class StartGroupTournamentSchema(BaseModel):
    event_name: str
    nomination_name: str
    type: NominationEventType

    group_count: int = Field(gt=0)


class GetGroupsOfTournamentSchema(BaseModel):
    groups: list[GroupSchema]

    class Config:
        from_attributes = True

