import datetime

from sqlalchemy.orm import Session

from db.models.nomination import Nomination
from db.models.team import Team
from db.schemas.nomination.nomination_get import NominationGetSchema


def create_missing_items(
        db: Session,
        model_name: type(Nomination),
        items: list[NominationGetSchema]
) -> list[type(Nomination)] | None:
    if not items:
        return None
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


def round_robin(teams: list[Team | None]):
    num_players = len(teams)
    matches = []

    if num_players % 2 != 0:
        teams.append(None)
        num_players += 1

    for _ in range(num_players - 1):
        mid = num_players // 2
        first_half = teams[:mid]
        second_half = teams[mid:]
        round_ = zip(first_half, reversed(second_half))
        matches.extend(round_)
        teams.insert(1, teams.pop())

    return [match for match in matches if match[0] is not None and match[1] is not None]


def get_person_age(birth_date: datetime.datetime):
    year, month, day = map(int, str(birth_date).split('-'))
    today = datetime.date.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age
