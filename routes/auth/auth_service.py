from sqlalchemy.orm import Session


class AuthServie:
    def __init__(self, db: Session):
        self.__db = db

    def login(self):
        pass

    def logout(self):
        pass

    def sign_in(self):
        pass

