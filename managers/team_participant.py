from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.team_participant.team_participant import append_participant_to_team_db, get_team_participant_db
from db.models.participant import Participant
from db.models.team import Team


class TeamParticipantManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__participant_already_in_team_error = "participant already in team"
        self.__participant_not_in_team_error = "participant not in team"

    def get_team_participant_of_raise_if_not_found(self, team_db: type(Team), participant_db: type(Participant)):
        team_participant_db = get_team_participant_db(self.__db, team_db, participant_db)
        if not team_participant_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__participant_not_in_team_error}
            )
        return team_participant_db

    def append_participant_to_team(self, participant_db: type(Participant), team_db: type(Team)):
        append_participant_to_team_db(self.__db, participant_db, team_db)

    def raise_exception_if_participant_already_in_team(self, participant_db: type(Participant), team_db: type(Team)):
        if team_db in set(participant_db.teams):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_already_in_team_error}
            )

    def raise_exception_if_participant_not_in_team(self, participant_db: type(Participant), team_db: type(Team)):
        if not (team_db in set(participant_db.teams)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_not_in_team_error}
            )

