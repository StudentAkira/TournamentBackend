from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.user import UserSchema, UserCreateSchema, EditUserSchema
from managers.token import TokenManager
from managers.user import UserManager


class UsersService:

    def __init__(self, db: Session):
        self.__db = db
        self.__user_manager = UserManager(self.__db)
        self.__token_manager = TokenManager(self.__db)

        self.__user_created_message = "user created"
        self.__user_data_updated_message = "user data updated"

    def edit_user_data(self, response: Response, token: str, user_data: EditUserSchema):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_email_taken(user_data)
        self.__user_manager.edit_user_data(user_data, decoded_token.user_id)
        return {"message": self.__user_data_updated_message}

    def get_user_data(self, response: Response, token: str) -> UserSchema:
        decoded_token = self.__token_manager.decode_token(token, response)
        user = self.__user_manager.get_user_by_id(decoded_token.user_id)
        self.__token_manager.check_if_token_exists_in_db(token)
        return UserSchema(
            email=user.email,
            first_name=user.first_name,
            second_name=user.second_name,
            third_name=user.third_name,
            phone=user.phone,
            role=user.role,
            educational_institution=user.educational_institution
        )

    def create_user(self, response: Response, user: UserCreateSchema, token: str) -> dict[str, str]:
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_is_not_admin(decoded_token.role)
        self.__user_manager.create_user(user)
        return {"message": self.__user_created_message}
