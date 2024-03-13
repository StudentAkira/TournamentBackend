from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from starlette.responses import Response
from config import settings
from db.schemas.user import UserLoginSchema
from managers.token import TokenManager
from managers.user import UserManager


class AuthService:
    def __init__(self, db: Session):
        self.__db = db
        self.__user_manager = UserManager(self.__db)
        self.__token_manager = TokenManager(self.__db)

        self.__logged_in_message = "logged in"
        self.__logged_out_message = "logged out"

    def login(self, response: Response, user_login: UserLoginSchema) -> dict[str, str]:
        user = self.__user_manager.get_user_by_email(user_login.email)
        self.__user_manager.raise_exception_if_user_not_found(user)
        self.__user_manager.check_user_password(user, user_login.password)
        user_id = self.__user_manager.get_user_id_associated_with_email(user)
        token = self.__token_manager.generate_token(user_id, user.role)
        expires = datetime.utcnow() + timedelta(days=settings.jwt_token_expiration_time_days)
        response.set_cookie(
            key="token",
            value=token,
            httponly=True,
            samesite="lax",
            secure=True,
            expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            domain="127.0.0.1"
        )
        return {"message": self.__logged_in_message}

    def logout(self, response: Response, token: str) -> dict[str, str]:
        self.__token_manager.decode_token(token, response)
        self.__token_manager.check_if_token_exists_in_db(token)
        self.__token_manager.delete_token_from_db(token)
        response.delete_cookie(key="token")
        return {"message": self.__logged_out_message}
