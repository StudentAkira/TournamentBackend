from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from starlette.responses import Response

from config import settings
from db.schemas.user import UserLoginSchema

from managers.token_manager import TokenManager
from managers.user_manager import UserManager


class AuthService:
    def __init__(self, db: Session):
        self.__db = db
        self.__user_manager = UserManager(self.__db)
        self.__token_manager = TokenManager(self.__db)

        self.__logged_in_message = "logged in"
        self.__logged_out_message = "logged out"

    def login(self, response: Response, user: UserLoginSchema) -> dict[str, str]:
        user_db = self.__user_manager.get_db_user_by_email(user.email)
        self.__user_manager.raise_exception_if_user_not_found(user_db)
        self.__user_manager.check_user_password(user_db, user.password)
        token = self.__token_manager.generate_token(user_db.id, user_db.role)
        expires = datetime.utcnow() + timedelta(days=settings.jwt_token_expiration_time_days)
        response.set_cookie(
            key="token",
            value=token,
            httponly=True,
            samesite="none",
            secure=True,
            expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
        )
        return {"message": self.__logged_in_message}

    def logout(self, response: Response, token) -> dict[str, str]:
        self.__token_manager.decode_token(token, response)
        self.__token_manager.get_token_db(token)
        self.__token_manager.delete_token_db(token)
        response.delete_cookie(key="token")
        return {"message": self.__logged_out_message}
