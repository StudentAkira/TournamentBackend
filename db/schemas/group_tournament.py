from pydantic import BaseModel, Field

from db.schemas.nomination_event import NominationEventType


class StartGroupTournamentSchema(BaseModel):
    event_name: str
    nomination_name: str
    type: NominationEventType

    group_count: int