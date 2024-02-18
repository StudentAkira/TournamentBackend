from sqlalchemy.orm import Session


class TokenManager:

    def __init__(self, db: Session):
        self.__db = db

    def generate_token(self):
        pass

    def decode_token(self):
        pass
