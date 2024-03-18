from typing import cast

from fastapi import HTTPException
from sqlalchemy import exists
from sqlalchemy.orm import Session
from starlette import status

from db.crud.nominations import get_nominations_db, \
    save_nominations_db, \
    get_nomination_by_name_db, \
    update_nomination_db, create_nomination_db
from db.models.nomination import Nomination
from db.schemas.nomination import NominationSchema


class NominationManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__nomination_does_not_exist_error = "nomination not found"
        self.__nomination_name_taken_error = "nomination name taken"

    def create(self, nomination: NominationSchema):
        create_nomination_db(self.__db, nomination)

    def create_many(self, nominations: list[NominationSchema]):
        save_nominations_db(self.__db, nominations)

    def list(self, offset: int, limit: int) -> list[NominationSchema]:
        nominations_db = get_nominations_db(self.__db, offset, limit)
        nominations = [NominationSchema.from_orm(nomination_db) for nomination_db in nominations_db]
        return nominations

    def read_by_name(self, name: str) -> NominationSchema | None:
        nomination_db = get_nomination_by_name_db(self.__db, name)
        if nomination_db:
            return NominationSchema.from_orm(nomination_db)

    def update(self, old_nomination: NominationSchema, new_nomination: NominationSchema):
        update_nomination_db(self.__db, old_nomination, new_nomination)

    def delete(self, nomination_name: str):
        pass

    def raise_exception_if_not_found(self, nomination_name: str):
        entity_exists = self.__db.query(
            exists().where(cast("ColumnElement[bool]", Nomination.name == nomination_name))).scalar()
        if not entity_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__nomination_does_not_exist_error}
            )

    def raise_exception_if_name_taken(self, nomination_name: str):
        entity_exists = self.__db.query(
            exists().where(cast("ColumnElement[bool]", Nomination.name == nomination_name))).scalar()
        if entity_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__nomination_name_taken_error}
            )
