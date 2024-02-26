from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db import models
from db.crud.nominations import get_nominations_db, save_nominations_db, get_nomination_by_name_db
from db.schemas.nomination import NominationSchema


class NominationManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__nomination_does_not_exist_error = "nomination not found"

    def get_nominations(self, offset: int, limit: int) -> list[NominationSchema]:
        nominations_db = get_nominations_db(self.__db, offset, limit)
        nominations = [NominationSchema.from_orm(nomination_db) for nomination_db in nominations_db]
        return nominations

    def create_nominations(self, nominations: list[NominationSchema]):
        save_nominations_db(self.__db, nominations)

    def get_nomination_by_name(self, name: str) -> NominationSchema | None:
        nomination_db = get_nomination_by_name_db(self.__db, name)
        if nomination_db:
            return NominationSchema.from_orm(nomination_db)

    def raise_exception_if_nomination_does_not_exist(self, name: str):
        nomination = self.get_nomination_by_name(name)
        if not nomination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__nomination_does_not_exist_error}
            )
