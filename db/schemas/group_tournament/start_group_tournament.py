from pydantic import BaseModel, Field

from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema


class StartGroupTournamentSchema(BaseModel):
    olympyc_nomination_event: OlympycNominationEventSchema

    group_count: int = Field(gt=0)
