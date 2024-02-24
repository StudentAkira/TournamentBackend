from sqlalchemy.orm import Session

from db.schemas import Team


class ParticipantManager:

    def __init__(self, db: Session):
        self.__db = db

    def get_participants(self, offset: int, limit: int):
        pass

    def create_participant(self, team: list[Team]):
        pass
