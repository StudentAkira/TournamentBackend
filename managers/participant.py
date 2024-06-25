from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from db.crud.participant.participant import get_participants_by_owner_db, create_participant_db, \
    get_participant_by_email_db, hide_participant_db, update_participant_db, get_participant_by_id_db
from db.models.participant import Participant
from db.models.user import User
from db.schemas.participant.participant_create import ParticipantCreateSchema
from db.schemas.participant.participant_get import ParticipantGetSchema
from db.schemas.participant.participant_update import ParticipantUpdateSchema
from db.schemas.user.user_role import UserRole


class ParticipantManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__email_taken_error = "email taken error"
        self.__participant_not_found_error = "participant does not exist"
        self.__wrong_participant_owner_error = "participant does not belongs to owner"

    def get_by_email_or_raise_if_not_found(self, email: EmailStr):
        participant_db = get_participant_by_email_db(self.__db, email)
        self.raise_exception_if_not_found(participant_db)
        return participant_db

    def get_by_id_or_raise_if_not_found(self, participant_id: int) -> Participant:
        participant_db = get_participant_by_id_db(self.__db, participant_id)
        self.raise_exception_if_not_found(participant_db)
        return participant_db

    def get_by_id(self, participant_id: int) -> Participant | None:
        participant_db = get_participant_by_id_db(self.__db, participant_id)
        return participant_db

    def list_by_owner(self, offset: int, limit: int, user_id: int) -> list[ParticipantGetSchema]:
        participants_db = get_participants_by_owner_db(self.__db, offset, limit, user_id)
        participants = [ParticipantGetSchema.from_orm(participant_db) for participant_db in participants_db]
        return participants

    def create(self, participant: ParticipantCreateSchema, creator_id):
        participant_db = get_participant_by_email_db(self.__db, participant.email)
        if participant_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__email_taken_error}
            )
        create_participant_db(self.__db, participant, creator_id)

    def read_by_email(self, email: EmailStr) -> ParticipantGetSchema | None:
        participant_db = get_participant_by_email_db(self.__db, email)
        if participant_db:
            return ParticipantGetSchema.from_orm(participant_db)

    def hide(self, participant_db: type(Participant)):
        hide_participant_db(self.__db, participant_db)

    def update(self, participant_db: type(Participant), participant_data: ParticipantUpdateSchema):
        update_participant_db(self.__db, participant_db, participant_data)

    def raise_exception_if_owner_wrong(self, participant_db: type(Participant), user_db: type(User)):
        if user_db.role != UserRole.admin and participant_db.creator_id != user_db.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__wrong_participant_owner_error}
            )

    def raise_exception_if_email_taken(self, participant_db: type(Participant)):
        if participant_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__email_taken_error}
            )

    def raise_exception_if_not_found(self, participant: Participant | None):
        if participant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__participant_not_found_error}
            )
