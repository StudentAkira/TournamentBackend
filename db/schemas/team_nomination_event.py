from pydantic import BaseModel, EmailStr


class AppendTeamParticipantNominationEventSchema(BaseModel):
    team_name: str | EmailStr
    participant_email: EmailStr
    nomination_name: str
    event_name: str
    software: str | None
    equipment: str | None


class ListTeamsOfNominationEventSchema(BaseModel):
    nomination_name: str
    event_name: str


class UpdateTeamParticipantNominationEventSchema(BaseModel):
    participant_email: EmailStr
    nomination_name: str
    event_name: str
    software: str | None
    equipment: str | None


class DeleteTeamParticipantNominationEventSchema(BaseModel):
    participant_email: EmailStr
    nomination_name: str
    event_name: str


