from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas import Team


class ParticipantManager:

    def __init__(self, db: Session):
        self.__db = db

    def get_my_participants(self, response: Response, token: str, offset: int, limit: int):
        pass

    def create_participant(self, participant):
        pass
