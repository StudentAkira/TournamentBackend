from sqlalchemy.orm import Session

from db import models
from db.schemas import UserCreate, UserDB, TokenDB
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user_db(db: Session, user: UserCreate) -> UserDB:
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,

        first_name=user.first_name,
        second_name=user.second_name,
        third_name=user.third_name,

        role=user.role,
        region=user.region,

    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username_db(db: Session, username: str) -> UserDB | None:
    user = db.query(models.User).filter(models.User.username == username).first()
    return user


def get_user_by_id_db(db: Session, user_id: int) -> UserDB | None:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


def save_token_db(db: Session, token: str, user_id: int) -> TokenDB:
    db_token = models.Token(
        token=token,
        owner_id=user_id
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def delete_token_db(db: Session, token: str):
    db_token = db.query(models.Token).filter(models.Token.token == token).first()
    if db_token:
        db.query(models.Token).filter(models.Token.token == token).delete()
    db.commit()


def get_token_db(db: Session, token: str) -> TokenDB:
    db_token = db.query(models.Token).filter(models.Token.token == token).first()
    return db_token
