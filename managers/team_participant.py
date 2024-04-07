from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from db.crud.team_participant.team_participant import append_participant_to_team_db, delete_participant_from_team_db, \
    check_if_participant_already_in_team_db
from db.schemas.participant.participant import ParticipantSchema
from db.schemas.team.team import TeamSchema


class TeamParticipantManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__participant_already_in_team_error = "participant already in team"
        self.__participant_not_in_team_error = "participant not in team"

    def append_participant_to_team(self, participant: ParticipantSchema, team: TeamSchema):
        append_participant_to_team_db(self.__db, participant, team)

    def delete_participant_from_team(self, participant_email: EmailStr, team_name: str):
        delete_participant_from_team_db(self.__db, participant_email, team_name)

    def raise_exception_if_participant_already_in_team(self, participant: ParticipantSchema, team: TeamSchema):
        if check_if_participant_already_in_team_db(self.__db, participant, team):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_already_in_team_error}
            )

    def raise_exception_if_participant_not_in_team(self, participant: ParticipantSchema, team: TeamSchema):
        if not check_if_participant_already_in_team_db(self.__db, participant, team):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_not_in_team_error}
            )
