from pydantic import EmailStr
from sqlalchemy.orm import Session

from db import models
from db.schemas import TokenDB, DatabaseUser, CreateUser, Event, Nomination, EventCreate
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
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email_db(db: Session, email: str) -> DatabaseUser | None:
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return DatabaseUser.from_orm(user)


def get_user_by_id_db(db: Session, user_id: int) -> DatabaseUser | None:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        return DatabaseUser.from_orm(user)


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


def get_events_db(db: Session, offset: int, limit: int) -> list[Event]:
    db_events = db.query(models.Event).offset(offset).limit(limit).all()
    events = [Event.from_orm(event) for event in db_events]
    return events


def get_nominations_db(db: Session, offset: int, limit: int):
    db_nominations = db.query(models.Nomination).offset(offset).limit(limit).all()
    nominations = [Nomination.from_orm(nomination) for nomination in db_nominations]
    return nominations


def create_nomination(db: Session, nomination: Nomination):
    db_nomination = models.Nomination(
        name=nomination.name
    )
    db.add(db_nomination)
    db.commit()
    db.refresh(db_nomination)
    return db_nomination

def get_or_create_nominations_db(db: Session, nominations: list[Nomination]):
    nomination_names = {nomination.name for nomination in nominations}
    nominations_ids = db.query(models.Nomination.id).all()
    return nominations_ids


def create_event_db(db: Session, event: EventCreate, owner_id: int):
    print(event.nominations)
    nominations_ids = get_or_create_nominations_db(db, event.nominations)
    print("Nominations queried :: ", nominations_ids)
    event = models.Event(
        owner_id=owner_id,
        name=event.name,
        nominations=[]
    )

    db.add(event)
    db.commit()
    db.refresh(event)
    return event
