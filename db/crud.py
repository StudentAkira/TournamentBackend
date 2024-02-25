from pydantic import EmailStr
from sqlalchemy.orm import Session

from db import models
from db.schemas import TokenDB, DatabaseUser, CreateUser, Event, BaseNomination, EventCreate, Team, Participant, \
    Software, Equipment
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
    nominations = [BaseNomination.from_orm(nomination) for nomination in db_nominations]
    return nominations


def get_nominations_by_names_db(db: Session, names: set[str]):
    db_nominations = db.query(models.Nomination).filter(models.Nomination.name.in_(names)).all()
    return db_nominations


def get_event_by_name_db(db: Session, name: str) -> models.Event | None:
    db_event = db.query(models.Event).filter(models.Event.name == name).first()
    return db_event


def save_nominations_db(db: Session, nominations: list[BaseNomination]):
    db_nominations = create_non_existent_return_all_nominations_db(db, nominations)
    db.commit()
    return db_nominations


def create_non_existent_return_all_nominations_db(db: Session, nominations: list[BaseNomination]):
    all_nominations = db.query(models.Nomination).all()
    existing_nominations_names = {db_nomination.name for db_nomination in all_nominations}

    new_nominations = [
        models.Nomination(name=nomination.name)
        for nomination in nominations
        if nomination.name not in existing_nominations_names
    ]
    received_nominations_names = {nomination.name for nomination in nominations}
    created_nominations_names = {nomination.name for nomination in new_nominations}

    existing_nominations = [nomination for nomination in db.query(models.Nomination). \
        filter(
        models.Nomination.name.in_(received_nominations_names - created_nominations_names)
    ).all()]

    for db_nomination in new_nominations:
        db.add(db_nomination)

    return existing_nominations + new_nominations


def create_event_db(db: Session, event: EventCreate, owner_id: int):
    nominations = event.nominations
    db_nominations = create_non_existent_return_all_nominations_db(db, nominations)
    db_event = models.Event(
        name=event.name,
        owner_id=owner_id
    )
    db_event.nominations.extend(db_nominations)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def append_event_nominations_db(db: Session, event: models.Event, nominations: list[BaseNomination]):
    db_nominations = create_non_existent_return_all_nominations_db(db, nominations)
    event.nominations.extend(set(db_nominations) - set(event.nominations))
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_team_by_name_db(db: Session, name: str) -> models.Team | None:
    team = db.query(models.Team).filter(models.Team.name == name).first()
    return team


def create_team_db(db: Session, team: Team) -> models.Team:
    db_team = models.Team(name=team.name)
    db.add(db_team)
    db.commit()
    return db_team


def create_software_db(db: Session, software: Software):
    pass


def create_equipment_db(db: Session, equipment: Equipment):
    pass


def create_participant_db(db: Session, participant: Participant):
    pass



