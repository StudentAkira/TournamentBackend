from pydantic import BaseModel, EmailStr


class AppendTeamToEventNominationSchema(BaseModel):
    team_name: str | EmailStr
    participant_emails: list[EmailStr]
    event_name: str
    nomination_name: str
    software: str | None
    equipment: str | None
