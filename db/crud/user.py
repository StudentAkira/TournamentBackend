from typing import cast

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db import models
from db.schemas.user import UserCreateSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user_db(db: Session, user: UserCreateSchema) -> type(models.User):
    hashed_password = pwd_context.hash(user.password)
    user_db = models.User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        second_name=user.second_name,
        third_name=user.third_name,
        phone=user.phone,
        educational_institution=user.educational_institution,
        role=user.role,
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def get_user_by_email_db(db: Session, email: str) -> type(models.User) | None:
    user_db = db.query(models.User).filter(
        cast("ColumnElement[bool]", models.User.email == email)
    ).first()
    if user_db:
        return user_db


def get_user_by_id_db(db: Session, user_id: int) -> type(models.User) | None:
    user_db = db.query(models.User).filter(
        cast("ColumnElement[bool]", models.User.id == user_id)
    ).first()
    if user_db:
        return user_db
