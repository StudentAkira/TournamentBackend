from sqlalchemy.orm import Session

from db.schemas import UserCreate, UserLogin, UserGet
from managers.token_manager import TokenManager
from managers.user_manager import UserManager


class AuthService:
    def __init__(self, db: Session):
        self.__db = db
        self.__user_manager = UserManager(self.__db)
        self.__token_manager = TokenManager(self.__db)

        self.__logged_out_message = "logged out"
        self.__admin_created_message = "admin created"
        self.__judge_created_message = "judge created"

    def get_user_data(self, token: str) -> dict[str, UserGet]:
        decoded = self.__token_manager.decode_token(token)
        db_user = self.__user_manager.get_user_by_id(decoded.get("user_id"))
        self.__token_manager.get_token_db(token)
        return {"data": db_user}

    def login(self, user: UserLogin) -> dict[str, str]:
        db_user = self.__user_manager.get_user_by_username(user.username)
        self.__user_manager.check_user_password(db_user, user.password)
        token = self.__token_manager.generate_token(db_user.id)
        return {"token": token}

    def logout(self, token) -> dict[str, str]:
        self.__token_manager.decode_token(token)
        self.__token_manager.get_token_db(token)
        self.__token_manager.delete_token_db(token)
        return {"message": self.__logged_out_message}

    def create_admin(self, user: UserCreate, secret) -> dict[str, str]:
        self.__user_manager.create_admin(user, secret)
        return {"message": self.__admin_created_message}

    def create_judge(self, user: UserCreate, token: str) -> dict[str, str]:
        decoded = self.__token_manager.decode_token(token)
        creator = self.__user_manager.get_user_by_id(decoded.get('user_id'))
        self.__user_manager.raise_exception_if_user_is_not_admin(creator)
        self.__user_manager.raise_exception_if_user_is_not_judge(user)
        self.__user_manager.create_judge(user)
        return {"message": self.__judge_created_message}
