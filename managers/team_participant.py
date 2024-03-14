from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.team_participant import append_participant_to_team_db, check_if_participant_already_in_team_db
from db.schemas.participant import ParticipantSchema
from db.schemas.team import TeamSchema


class TeamParticipantManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__participant_already_in_team_error = "participant already in team"

    def append_participant_to_team(self, participant: ParticipantSchema, team: TeamSchema):
        append_participant_to_team_db(self.__db, participant, team)

    def raise_exception_if_participant_already_in_team(self, participant: ParticipantSchema, team: TeamSchema):
        if check_if_participant_already_in_team_db(self.__db, participant, team):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_already_in_team_error}
            )
