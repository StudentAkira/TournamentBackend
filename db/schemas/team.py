from pydantic import BaseModel, Field, EmailStr

from db.schemas.participant import ParticipantSchema


class TeamSchema(BaseModel):
    name: str = Field(min_length=3)

    class Config:
        from_attributes = True


class AppendTeamToEventNominationSchema(BaseModel):
    team_name: str | EmailStr
    participant_emails: list[EmailStr]
    event_name: str
    nomination_name: str
    software: str | None
    equipment: str | None
