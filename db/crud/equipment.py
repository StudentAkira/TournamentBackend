from typing import cast

from sqlalchemy.orm import Session

from db import models
from db.crud.general import create_missing_items
from db.schemas.equipment import EquipmentSchema


def create_equipment_missing_in_db(db: Session, equipments: list[EquipmentSchema]) -> list[type(models.Equipment)]:
    equipment = create_missing_items(db, models.Equipment, equipments)
    db.commit()
    return equipment


def get_equipment_db(db: Session, offset: int, limit: int) -> list[type(models.Equipment)]:
    equipment = db.query(models.Equipment).offset(offset).limit(limit).all()
    return equipment


def get_equipment_by_name_db(db: Session, name: str) -> type(models.Equipment):
    equipment = db.query(models.Equipment).filter(
        cast("ColumnElement[bool]", models.Equipment.name == name)
    ).first()
    return equipment
