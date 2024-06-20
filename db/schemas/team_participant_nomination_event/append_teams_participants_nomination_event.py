from pydantic import BaseModel

from db.schemas.nomination_event.nomination_event import NominationEventSchema
from db.schemas.team_participant.team_participant_append import TeamParticipantAppendSchema


class TeamParticipantNominationEventAppendSchema(BaseModel):
    nomination_event: NominationEventSchema
    team_id: int
    team_participants: list[TeamParticipantAppendSchema]

    def to_nomination_event_schema(self):
        return NominationEventSchema(
            event_id=self.nomination_event.event_id,
            nomination_id=self.nomination_event.nomination_id,
            type=self.nomination_event.type
        )

