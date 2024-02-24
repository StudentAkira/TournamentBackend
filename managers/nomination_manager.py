from sqlalchemy.orm import Session

from db.crud import get_nominations_db, save_nominations_db
from db.schemas import BaseNomination


class NominationManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__nominations_created_message = "nominations created"

    def get_nominations(self, offset: int, limit: int):
        nominations = get_nominations_db(self.__db, offset, limit)
        return nominations

    def create_nominations(self, nominations: list[BaseNomination]):
        save_nominations_db(self.__db, nominations)
        return {"message": self.__nominations_created_message}
