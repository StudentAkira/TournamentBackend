from sqlalchemy.orm import Session

from db import models
from db.crud.software import get_software_db, create_software_missing_in_db
from db.schemas.software import SoftwareSchema


class SoftwareManager:
    def __init__(self, db: Session):
        self.__db = db



    def get_softwares(self, offset: int, limit: int) -> list[SoftwareSchema]:
        softwares_db = get_software_db(self.__db, offset, limit)
        softwares = [SoftwareSchema.from_orm(software_db) for software_db in softwares_db]
        return softwares

    def create_software(self, software: list[SoftwareSchema]):
        create_software_missing_in_db(self.__db, software)
