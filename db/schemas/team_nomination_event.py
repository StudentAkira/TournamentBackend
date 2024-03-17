from pydantic import BaseModel, EmailStr


class AppendTeamParticipantNominationEventSchema(BaseModel):
    team_name: str | EmailStr
    participant_email: EmailStr
    event_name: str
    nomination_name: str
    software: str | None
    equipment: str | None


class ListTeamsOfNominationEventSchema(BaseModel):
    nomination_name: str
    event_name: str


class DeleteTeamParticipantNominationEventSchema(BaseModel):
    team_name: str | EmailStr
    participant_email: EmailStr
    event_name: str
    nomination_name: str

