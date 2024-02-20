from sqlalchemy.orm import Session

from db import models
from db.schemas import TokenDB, DatabaseUser, CreateUser
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user_db(db: Session, user: CreateUser) -> DatabaseUser:
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        second_name=user.second_name,
        third_name=user.third_name,
        phone=user.phone,
        educational_institution=user.educational_institution,
        region=user.region,
        role=user.role,

    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email_db(db: Session, email: str) -> DatabaseUser | None:
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return DatabaseUser(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            first_name=user.first_name,
            second_name=user.second_name,
            third_name=user.third_name,
            phone=user.phone,
            role=user.role,
            region=user.region,
            educational_institution=user.educational_institution
        )


def get_user_by_id_db(db: Session, user_id: int) -> DatabaseUser | None:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        return DatabaseUser(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            first_name=user.first_name,
            second_name=user.second_name,
            third_name=user.third_name,
            phone=user.phone,
            role=user.role,
            region=user.region,
            educational_institution=user.educational_institution
        )


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
