from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.user.edit_user import EditUserSchema
from db.schemas.user.user import UserSchema
from db.schemas.user.user_create import UserCreateSchema
from managers.token import TokenManager
from managers.user import UserManager


class UsersService:

    def __init__(self, db: Session):
        self.__db = db
        self.__user_manager = UserManager(self.__db)
        self.__token_manager = TokenManager(self.__db)

        self.__user_created_message = "user created"
        self.__user_data_updated_message = "user data updated"

    def create_user(self, response: Response, user: UserCreateSchema, token: str) -> dict[str, str]:
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_is_not_admin(decoded_token.role)
        self.__user_manager.create_user(user)
        return {"message": self.__user_created_message}

    def get_user_data(self, response: Response, token: str) -> UserSchema:
        decoded_token = self.__token_manager.decode_token(token, response)
        user_db = self.__user_manager.get_user_by_id_or_raise_if_not_found(decoded_token.user_id)
        self.__token_manager.get_or_raise_if_not_found(token)
        return user_db

    def list(self, response: Response, token: str) -> list[UserSchema]:
        self.__token_manager.decode_token(token, response)
        return self.__user_manager.list()

    def edit_user_data(self, response: Response, token: str, user_data: EditUserSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.edit_user_data(user_data, decoded_token.user_id)
        return {"message": self.__user_data_updated_message}
