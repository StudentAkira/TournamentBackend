from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.nomination.nomination import get_nominations_db, \
    update_nomination_db, create_nomination_db, get_event_related_nominations, \
    get_event_related_nominations_starts_with, get_event_not_related_nominations_starts_with, \
    get_event_not_related_nominations, get_nomination_by_name_and_user_id_db
from db.models.nomination import Nomination
from db.schemas.nomination.nomination import NominationSchema


class NominationManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__nomination_does_not_exist_error = "nomination not found"
        self.__nomination_name_taken_error = "nomination name taken"

    def create(self, user_id: int, nomination: NominationSchema):
        create_nomination_db(self.__db, user_id, nomination)

    def list(self, user_id: int, offset: int, limit: int) -> list[NominationSchema]:
        nominations_db = get_nominations_db(self.__db, user_id, offset, limit)
        nominations = [NominationSchema.from_orm(nomination_db) for nomination_db in nominations_db]
        return nominations

    def get_or_create(self, user_id: int, nomination_name: str):
        nomination_db = get_nomination_by_name_and_user_id_db(self.__db, user_id, nomination_name)
        if nomination_db is None:
            self.create(user_id, NominationSchema(name=nomination_name))
            nomination_db = self.get_by_name_and_user_id_or_raise_exception_if_not_found(user_id, nomination_name)
        return nomination_db

    def get_by_name_and_user_id_or_raise_exception_if_not_found(self, user_id: int, name: str) -> type(Nomination):
        nomination_db = get_nomination_by_name_and_user_id_db(self.__db, user_id, name)
        if not nomination_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__nomination_does_not_exist_error}
            )
        return nomination_db

    def update(self, nomination_db: type(Nomination), new_nomination: NominationSchema):
        update_nomination_db(self.__db, nomination_db, new_nomination)

    def get_event_related_nominations(self, event_db, offset, limit):
        nominations_db = get_event_related_nominations(self.__db, event_db, offset, limit)
        return nominations_db

    def get_event_not_related_nominations(self, event_db, offset, limit):
        nominations_db = get_event_not_related_nominations(self.__db, event_db, offset, limit)
        return nominations_db

    def get_event_related_nominations_starts_with(self, event_db, title, offset, limit):
        nominations_db = get_event_related_nominations_starts_with(self.__db, event_db, title, offset, limit)
        return nominations_db

    def get_event_not_related_nominations_starts_with(self, event_db, title, offset, limit):
        nominations_db = get_event_not_related_nominations_starts_with(self.__db, event_db, title, offset, limit)
        return nominations_db

    def raise_exception_if_name_taken(self, nomination_db: Nomination | None):
        if nomination_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__nomination_name_taken_error}
            )



