from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from db.crud.participant import get_participants_by_owner_db, create_participant_db, get_participant_by_email_db, \
    append_participant_to_team_db, check_if_participant_already_in_team_db
from db.schemas.participant import ParticipantSchema
from db.schemas.team import TeamSchema


class ParticipantManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__email_taken_error = "email taken error"
        self.__participant_not_found_error = "participant does not exist"
        self.__wrong_participant_owner_error = "participant does not belongs to owner"
        self.__participant_already_in_team_error = "participant already in team"

    def get_participants_by_owner(self, offset: int, limit: int, user_id: int) -> list[ParticipantSchema]:
        participants_db = get_participants_by_owner_db(self.__db, offset, limit, user_id)
        participants = [ParticipantSchema.from_orm(participant_db) for participant_db in participants_db]
        return participants

    def create_participant(self, participant: ParticipantSchema, creator_id):
        self.raise_exception_if_email_taken(participant.email)
        create_participant_db(self.__db, participant, creator_id)

    def get_participant_by_email(self, email: EmailStr) -> ParticipantSchema | None:
        participant_db = get_participant_by_email_db(self.__db, email)
        if participant_db:
            return ParticipantSchema.from_orm(participant_db)

    def append_participant_to_team(self, participant: ParticipantSchema, team: TeamSchema):
        append_participant_to_team_db(self.__db, participant, team)

    def raise_exception_if_email_taken(self, email: EmailStr):
        participant = self.get_participant_by_email(email)
        if participant:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__email_taken_error}
            )

    def raise_exception_if_participant_owner_wrong(self, participant_email: EmailStr, creator_id: int):
        participant_db = get_participant_by_email_db(self.__db, participant_email)
        if participant_db.creator_id != creator_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__wrong_participant_owner_error}
            )

    def raise_exception_if_participant_not_found(self, participant_email: EmailStr):
        participant = self.get_participant_by_email(participant_email)
        if not participant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__participant_not_found_error}
            )

    def raise_exception_if_participant_already_in_team(self, participant: ParticipantSchema, team: TeamSchema):
        if check_if_participant_already_in_team_db(self.__db, participant, team):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_already_in_team_error}
            )

