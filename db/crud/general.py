from sqlalchemy.orm import Session

from db import models
from db.schemas.equipment import EquipmentSchema
from db.schemas.nomination import NominationSchema
from db.schemas.software import SoftwareSchema


def create_missing_items(
        db: Session,
        model_name: type(models.Equipment) | type(models.Software) | type(models.Nomination),
        items: list[EquipmentSchema | SoftwareSchema | NominationSchema]
) -> list[type(models.Equipment) | type(models.Software) | type(models.Nomination)]:
    all_items = db.query(model_name).all()
    existing_items_names = {db_item.name for db_item in all_items}

    new_items = [
        model_name(name=item.name)
        for item in items
        if item.name not in existing_items_names
    ]
    received_items_names = {item.name for item in items}
    created_items_names = {item.name for item in new_items}

    existing_items = [
        item for item in db.query(model_name).filter(
            model_name.name.in_(received_items_names - created_items_names)
        ).all()
    ]

    for db_item in new_items:
        db.add(db_item)

    return existing_items + new_items
