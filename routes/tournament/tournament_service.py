from sqlalchemy.orm import Session


class TournamentService:

    def __init__(self, db: Session):
        self.__db = db
