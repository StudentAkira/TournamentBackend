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


def get_user_by_email_db(db: Session, email: str) -> models.User | None:
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return user


def get_user_by_id_db(db: Session, user_id: int) -> models.User | None:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
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
    nominations = create_missing_items(db, models.Nomination, nominations)
    return nominations


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


def get_my_teams_db(db: Session, offset: int, limit: int, owner_id: int):
    teams_db = db.query(models.Team).filter(models.Team.creator_id == owner_id).offset(offset).limit(limit).all()
    teams = [Team.from_orm(team_db) for team_db in teams_db]
    return teams


def create_team_db(db: Session, team: Team, creator_id: int) -> models.Team:
    creator = get_user_by_id_db(db, creator_id)
    db_team = models.Team(name=team.name)
    db_team.creator = creator
    db.add(db_team)
    db.commit()
    return db_team


def get_software_by_name_db(db: Session, name: str):
    software = db.query(models.Software).filter(models.Software.name == name).first()
    return software


def create_software_db(db: Session, softwares: list[Software]):
    software = create_missing_items(db, models.Software, softwares)
    db.commit()
    return software

def get_equipment_by_name_db(db: Session, name: str):
    equipment = db.query(models.Equipment).filter(models.Equipment.name == name).first()
    return equipment


def create_equipment_db(db: Session, equipments: list[Equipment]):
    equipment = create_missing_items(db, models.Equipment, equipments)
    db.commit()
    return equipment


def create_missing_items(
        db: Session,
        model_name: type(models.Equipment) | type(models.Software) | type(models.Nomination),
        items: list[Equipment | Software | BaseNomination]
):
    all_items = db.query(model_name).all()
    existing_items_names = {db_item.name for db_item in all_items}

    new_items = [
        model_name(name=item.name)
        for item in items
        if item.name not in existing_items_names
    ]
    received_items_names = {item.name for item in items}
    created_items_names = {item.name for item in new_items}

    existing_items = [item for item in db.query(model_name). \
        filter(
        model_name.name.in_(received_items_names - created_items_names)
    ).all()]

    for db_item in new_items:
        db.add(db_item)

    return existing_items + new_items


def create_participant_db(db: Session, participant: Participant):
    pass


def append_teams_for_participant(db: Session, teams: list[Team], participant: Participant):
    pass


def append_participants_for_team(db: Session, participants: list[Participant], team: Team):
    pass
