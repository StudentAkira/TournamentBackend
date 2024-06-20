from pydantic import BaseModel


class TeamParticipantAppendSchema(BaseModel):
    participant_id: int
    team_id: int
