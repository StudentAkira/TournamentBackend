from sqlalchemy.orm import Session

from db.schemas import Team


class TeamManager:

    def __init__(self, db: Session):
        self.__db = db

    def get_teams(self, offset: int, limit: int):
        pass

    def create_teams(self, team: list[Team]):
        pass
