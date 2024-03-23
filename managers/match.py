from sqlalchemy.orm import Session

from db.crud.match import get_group_matches_of_tournament_db
from db.schemas.group_tournament import GroupMatchSchema
from db.schemas.match import MatchSchema
from db.schemas.nomination_event import NominationEventSchema


class MatchManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

    def get_group_matches_of_tournament(self, nomination_event: NominationEventSchema):
        data = get_group_matches_of_tournament_db(self.__db, nomination_event)
        return data
