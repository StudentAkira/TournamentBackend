from pydantic import BaseModel, EmailStr


class AppendTeamToEventNominationSchema(BaseModel):
    team_name: str | EmailStr
    participant_emails: list[EmailStr]
    event_name: str
    nomination_name: str
    software: str | None
    equipment: str | None


class ListTeamsOfNominationEventSchema(BaseModel):
    nomination_name: str
    event_name: str


class UpdateTeamOfNominationEventSchema(BaseModel):
    team_name: str | EmailStr
    participant_emails: list[EmailStr]
    nomination_name: str
    event_name: str


class DeleteTeamFromNominationEvent(BaseModel):
    team_name: str
    event_name: str
    nomination_name: str
