from pydantic import BaseModel

from db.schemas.participant.participant_pdf import ParticipantPDFSchema


class NominationEventPDFSchema(BaseModel):
    nomination_name: str
    event_name: str
    type: str
    participants: list[ParticipantPDFSchema]

    first_name: str
    second_name: str
    third_name: str
    region: str
