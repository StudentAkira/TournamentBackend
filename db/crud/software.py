from typing import cast

from sqlalchemy.orm import Session

from db import models
from db.crud.general import create_missing_items
from db.schemas.software import SoftwareSchema


def create_software_missing_in_db(db: Session, softwares: list[SoftwareSchema]) -> list[type(models.Software)]:
    software = create_missing_items(db, models.Software, softwares)
    db.commit()
    return software


def get_software_by_name_db(db: Session, name: str) -> type(models.Software):
    software = db.query(models.Software).filter(
        cast("ColumnElement[bool]", models.Software.name == name)
    ).first()
    return software


def get_software_db(db: Session, offset: int, limit: int) -> list[type(models.Software)]:
    software_db = db.query(models.Software).offset(offset).limit(limit).all()
    software = [SoftwareSchema.from_orm(software_db) for software_db in software_db]
    return software
