from sqlalchemy.orm import Session


class UserManager:

    def __init__(self, db: Session):
        self.__db = db

    def login_user(self):
        pass

    def logout_user(self):
        pass

    def sign_in_user(self):
        pass
