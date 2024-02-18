from sqlalchemy.orm import Session

from db import models
from db.schemas import UserCreate, UserDB
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserCreate) -> UserDB:
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


def get_user_by_username(db: Session, username) -> UserDB | None:
    user = db.query(models.User).filter(models.User.username == username).first()
    return user
