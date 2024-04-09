from pydantic import BaseModel

from db.schemas.nomination_event.olympyc_nomination_event import OlympycNominationEventSchema


class StartGroupTournamentSchema(BaseModel):
    olympyc_nomination_event: OlympycNominationEventSchema
