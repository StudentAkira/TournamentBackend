from starlette.responses import Response

from db.schemas.equipment import EquipmentSchema
from managers.equipment_manager import EquipmentManager
from managers.token_manager import TokenManager


class EquipmentService:
    def __init__(self, db):
        self.__db = db
        self.__token_manager = TokenManager(db)
        self.__equipment_manager = EquipmentManager(db)

        self.__equipment_created_message = "equipment created"

    def get_equipment(self, response: Response, offset: int, limit: int, token: str):
        self.__token_manager.decode_token(token, response)
        return self.__equipment_manager.get_equipment(offset, limit)

    def create_equipment(self, response: Response, token: str, equipment: list[EquipmentSchema]):
        self.__token_manager.decode_token(token, response)
        self.__equipment_manager.create_equipment(equipment)
        return {"message": self.__equipment_created_message}

