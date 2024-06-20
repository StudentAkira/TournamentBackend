from pydantic import BaseModel

from db.schemas.participant.participant_create import ParticipantCreateSchema


class ParticipantUpdateSchema(BaseModel):
    id: int
    participant_data: ParticipantCreateSchema
