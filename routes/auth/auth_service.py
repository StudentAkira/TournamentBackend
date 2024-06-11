from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from starlette.responses import Response

from config import get_settings
from db.schemas.user.user_login import UserLoginSchema
from managers.token import TokenManager
from managers.user import UserManager


settings = get_settings()


class AuthService:
    def __init__(self, db: Session):
        self.__db = db
        self.__user_manager = UserManager(self.__db)
        self.__token_manager = TokenManager(self.__db)

        self.__logged_in_message = "logged in"
        self.__logged_out_message = "logged out"

    def login(self, response: Response, user_login: UserLoginSchema) -> dict[str, str]:
        user_db = self.__user_manager.get_user_by_email_or_raise_if_not_found(user_login.email)
        self.__user_manager.check_user_password(user_db, user_login.password)
        token = self.__token_manager.generate_token(user_db.id, user_db.role)
        expires = datetime.utcnow() + timedelta(days=settings.jwt_token_expiration_time_days + 1)
        response.set_cookie(
            key="token",
            value=token,
            httponly=True,
            samesite="lax",
            secure=False,
            expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            domain=settings.frontend_domain
        )
        return {"message": self.__logged_in_message}

    def logout(self, response: Response, token: str) -> dict[str, str]:
        response.delete_cookie(key="token")
        self.__token_manager.decode_token(token, response)
        token_db = self.__token_manager.get_or_raise_if_not_found(response, token)
        self.__token_manager.delete_token_from_db(token_db)
        return {"message": self.__logged_out_message}
