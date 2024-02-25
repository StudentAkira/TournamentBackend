from sqlalchemy.orm import Session
from starlette.responses import Response

from db.crud import create_equipment_db
from db.schemas import Equipment


class EquipmentManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__equipment_created_message = "equipment created"

    def get_equipments(self, offset: int, limit: int):
        pass

    def create_equipment(self, equipments: list[Equipment]):
        create_equipment_db(self.__db, equipments)
        return {"message": self.__equipment_created_message}
