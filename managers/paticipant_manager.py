from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from db import models
from db.crud.participant import get_participants_by_owner_db, create_participant_db, get_participant_by_email_db
from db.schemas.participant import ParticipantSchema


class ParticipantManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__email_taken_error = "email taken error"

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

    def raise_exception_if_email_taken(self, email: EmailStr):
        participant = self.get_participant_by_email(email)
        if participant:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__email_taken_error}
            )
