from sqlalchemy.orm import Session
from db.schemas import BaseUser, CreateUser
from managers.token_manager import TokenManager
from managers.user_manager import UserManager


class UsersService:

    def __init__(self, db: Session):
        self.__db = db
        self.__user_manager = UserManager(self.__db)
        self.__token_manager = TokenManager(self.__db)

        self.__user_created_message = "user created"

    def get_user_data(self, token: str) -> BaseUser:
        decoded = self.__token_manager.decode_token(token)
        db_user = self.__user_manager.get_user_by_id(decoded.get("user_id"))
        self.__token_manager.get_token_db(token)
        user = BaseUser.parse_obj(db_user)
        return user

    def create_user(self, user: CreateUser, token: str) -> dict[str, str]:
        decoded = self.__token_manager.decode_token(token)
        self.__user_manager.raise_exception_if_user_is_not_admin(decoded.role)
        self.__user_manager.create_user(user)
        return {"message": self.__user_created_message}
