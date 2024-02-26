from sqlalchemy.orm import Session

from db.crud.equipment import get_equipment_db, create_equipment_missing_in_db
from db.schemas.equipment import EquipmentSchema


class EquipmentManager:

    def __init__(self, db: Session):
        self.__db = db

    def get_equipment(self, offset: int, limit: int) -> list[EquipmentSchema]:
        equipments_db = get_equipment_db(self.__db, offset, limit)
        equipment = [EquipmentSchema.from_orm(equipment_db) for equipment_db in equipments_db]
        return equipment

    def create_equipment(self, equipment: list[EquipmentSchema]) -> dict[str, str]:
        create_equipment_missing_in_db(self.__db, equipment)
