from db.schemas import Participant


class ParticipationsService:

    def __init__(self, db):
        self.__db = db

    def create_participant(self, participant: Participant, token: str) -> dict[str, str]:
        pass

    def get_all_participants(self, token: str) -> list[Participant]:
        pass
