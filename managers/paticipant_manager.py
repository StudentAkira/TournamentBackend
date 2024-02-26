from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from db.crud import get_participant_by_email_db, create_participant_db, get_my_particiapnts_db
from db.schemas import Team, Participant


class ParticipantManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__participant_created_message = "participant created"
        self.__email_taken_error = "email taken error"

    def get_my_participants(self, user_id: int,  offset: int, limit: int):
        return get_my_particiapnts_db(self.__db, user_id, offset, limit)

    def create_participant(self, participant: Participant, creator_id):
        self.raise_exception_if_email_taken(participant.email)
        create_participant_db(self.__db, participant, creator_id)
        return {"message": self.__participant_created_message}

    def get_participant_by_name(self, email: EmailStr):
        return get_participant_by_email_db(self.__db, email)

    def raise_exception_if_email_taken(self, email: EmailStr):
        participant = self.get_participant_by_name(email)
        if participant:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__email_taken_error}
            )
