from sqlalchemy.orm import Session
from starlette.responses import Response

from db.crud import create_software_db, get_software_db
from db.schemas import Software


class SoftwareManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__software_created_message = "software created"

    def get_softwares(self, offset: int, limit: int):
        return get_software_db(self.__db, offset, limit)

    def create_software(self, software: list[Software]):
        create_software_db(self.__db, software)
        return {"message": self.__software_created_message}
