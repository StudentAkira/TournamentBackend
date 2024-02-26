from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud import get_nominations_db, save_nominations_db, get_nomination_by_name_db
from db.schemas import BaseNomination


class NominationManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__nominations_created_message = "nominations created"

        self.__nomination_does_not_exist_error = "nomination not found"

    def get_nominations(self, offset: int, limit: int):
        nominations = get_nominations_db(self.__db, offset, limit)
        return nominations

    def create_nominations(self, nominations: list[BaseNomination]):
        save_nominations_db(self.__db, nominations)
        return {"message": self.__nominations_created_message}

    def get_nomination_by_name(self, name: str):
        nomination = get_nomination_by_name_db(self.__db, name)
        return nomination

    def raise_exception_if_nomination_does_not_exist(self, name: str):
        nomination = self.get_nomination_by_name(name)
        if not nomination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"errror": self.__nomination_does_not_exist_error}
            )