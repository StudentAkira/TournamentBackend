from sqlalchemy.orm import Session

from db.schemas import UserCreate
from managers.token_manager import TokenManager
from managers.user_manager import UserManager


class AuthService:
    def __init__(self, db: Session):
        self.__db = db
        self.__user_manager = UserManager(self.__db)
        self.__token_manager = TokenManager(self.__db)

    def login(self):
        pass

    def logout(self):
        pass

    def sign_in(self, user: UserCreate, secret):
        self.__user_manager.create_user(user, secret)
        return {"message": "user created"}

