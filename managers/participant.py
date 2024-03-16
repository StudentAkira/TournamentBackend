from typing import cast

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import exists, and_
from sqlalchemy.orm import Session
from starlette import status

from db.crud.participant import get_participants_by_owner_db, create_participant_db, get_participant_by_email_db, \
    hide_participant_db
from db.models.participant import Participant
from db.schemas.participant import ParticipantSchema, ParticipantHideSchema


class ParticipantManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__email_taken_error = "email taken error"
        self.__participant_not_found_error = "participant does not exist"
        self.__wrong_participant_owner_error = "participant does not belongs to owner"

    def list_by_owner(self, offset: int, limit: int, user_id: int) -> list[ParticipantSchema]:
        participants_db = get_participants_by_owner_db(self.__db, offset, limit, user_id)
        participants = [ParticipantSchema.from_orm(participant_db) for participant_db in participants_db]
        return participants

    def create(self, participant: ParticipantSchema, creator_id):
        self.raise_exception_if_email_taken(participant.email)
        create_participant_db(self.__db, participant, creator_id)

    def read_by_email(self, email: EmailStr) -> ParticipantSchema | None:
        participant_db = get_participant_by_email_db(self.__db, email)
        if participant_db:
            return ParticipantSchema.from_orm(participant_db)

    def hide(self, participant_data: ParticipantHideSchema):
        hide_participant_db(self.__db, participant_data)

    def raise_exception_if_email_taken(self, email: EmailStr):
        entity_exists = self.__db.query(
            exists().where(cast("ColumnElement[bool]", Participant.email == email))).scalar()
        if entity_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__email_taken_error}
            )

    def raise_exception_if_owner_wrong(self, participant_email: EmailStr, creator_id: int):
        participant_db = get_participant_by_email_db(self.__db, participant_email)
        if participant_db.creator_id != creator_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__wrong_participant_owner_error}
            )

    def raise_exception_if_not_found(self, email: EmailStr):
        entity_exists = self.__db.query(
            exists().where(
                cast("ColumnElement[bool]", Participant.email == email)
            ).where(
                cast("ColumnElement[bool]", Participant.hidden == "f")
            )
        ).scalar()
        if not entity_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__participant_not_found_error}
            )
