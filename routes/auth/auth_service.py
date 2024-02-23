from sqlalchemy.orm import Session

from db.schemas import LoginUser
from managers.token_manager import TokenManager
from managers.user_manager import UserManager


class AuthService:
    def __init__(self, db: Session):
        self.__db = db
        self.__user_manager = UserManager(self.__db)
        self.__token_manager = TokenManager(self.__db)

        self.__logged_out_message = "logged out"

    def login(self, user: LoginUser) -> dict[str, str]:
        db_user = self.__user_manager.get_user_by_email(user.email)
        self.__user_manager.check_user_password(db_user, user.password)
        token = self.__token_manager.generate_token(db_user.id, db_user.role)
        return {"token": token}

    def logout(self, token) -> dict[str, str]:
        self.__token_manager.decode_token(token)
        self.__token_manager.get_token_db(token)
        self.__token_manager.delete_token_db(token)
        return {"message": self.__logged_out_message}
