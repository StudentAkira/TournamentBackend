from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.nominations import get_nominations_db, save_nominations_db, get_nomination_by_name_db, \
    nomination_exists_db, update_nomination_db
from db.schemas.nomination import NominationSchema


class NominationManager:
    def __init__(self, db: Session):
        self.__db = db

        self.__nomination_does_not_exist_error = "nomination not found"
        self.__nomination_name_taken_error = "nomination name taken"

    def create_nominations(self, nominations: list[NominationSchema]):
        save_nominations_db(self.__db, nominations)

    def get_nominations(self, offset: int, limit: int) -> list[NominationSchema]:
        nominations_db = get_nominations_db(self.__db, offset, limit)
        nominations = [NominationSchema.from_orm(nomination_db) for nomination_db in nominations_db]
        return nominations

    def get_nomination_by_name(self, name: str) -> NominationSchema | None:
        nomination_db = get_nomination_by_name_db(self.__db, name)
        if nomination_db:
            return NominationSchema.from_orm(nomination_db)

    def update_nomination(self, old_nomination: NominationSchema, new_nomination: NominationSchema):
        update_nomination_db(self.__db, old_nomination, new_nomination)

    def delete_nomination(self, nomination_name: str):
        pass

    def raise_exception_if_nomination_not_found(self, name: str):
        nomination = self.get_nomination_by_name(name)
        if not nomination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__nomination_does_not_exist_error}
            )

    def raise_exception_if_nomination_name_taken(self, nomination_name):
        if nomination_exists_db(self.__db, nomination_name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__nomination_name_taken_error}
            )
