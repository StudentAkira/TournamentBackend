from typing import cast

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db.models.user import User
from db.schemas.user import UserCreateSchema, EditUserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user_db(db: Session, user: UserCreateSchema) -> type(User):
    hashed_password = pwd_context.hash(user.password)
    user_db = User(
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


def get_users_db(db: Session):
    users_db = db.query(User).all()
    return users_db


def get_user_by_email_db(db: Session, email: str) -> type(User) | None:
    user_db = db.query(User).filter(
        cast("ColumnElement[bool]", User.email == email)
    ).first()
    if user_db:
        return user_db


def get_user_by_id_db(db: Session, user_id: int) -> type(User) | None:
    user_db = db.query(User).filter(
        cast("ColumnElement[bool]", User.id == user_id)
    ).first()
    if user_db:
        return user_db


def edit_user_data_db(db: Session, user_data: EditUserSchema, user_id: int):
    user_db = db.query(User).filter(cast("ColumnElement[bool]", User.id == user_id)).first()
    user_db.email = user_data.email if user_data.email else user_db.email
    user_db.hashed_password = pwd_context.hash(user_data.password) if user_data.password else user_db.hashed_password
    user_db.first_name = user_data.first_name if user_data.first_name else user_db.first_name
    user_db.second_name = user_data.second_name if user_data.second_name else user_db.second_name
    user_db.third_name = user_data.third_name if user_data.third_name else user_db.third_name
    user_db.phone = user_data.phone if user_data.phone else user_db.phone
    user_db.educational_institution = user_data.educational_institution if user_data.educational_institution else user_db.educational_institution
    db.add(user_db)
    db.commit()
