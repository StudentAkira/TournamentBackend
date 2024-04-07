from pydantic import BaseModel, EmailStr


class ParticipantHideSchema(BaseModel):
    participant_email: EmailStr
