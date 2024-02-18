import secrets

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from config import settings
from db.crud import create_user, get_user_by_username
from db.schemas import UserCreate, UserRole


class UserManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__wrong_secret_error = "wrong secret"
        self.__username_taken_error = "username taken"
        self.__secret_missing_error = "secret missing"
        self.__invalid_role_error = "invalid role"

    def login_user(self):
        pass

    def logout_user(self):
        pass

    def create_user(self, user: UserCreate, secret: str | None):
        self.raise_error_if_username_taken(user.username)
        if user.role == UserRole.admin:
            self.raise_error_if_secret_is_none(secret)
            self.check_secret_for_superuser_creation(secret)
        create_user(self.__db, user)

    def check_secret_for_superuser_creation(self, secret: str):
        match = secrets.compare_digest(secret, settings.app_secret_key)
        if not match:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": self.__wrong_secret_error}
            )

    def raise_error_if_username_taken(self, username):
        db_user = get_user_by_username(self.__db, username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__username_taken_error}
            )

    def raise_error_if_secret_is_none(self, secret):
        if not secret:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"error": self.__secret_missing_error}
            )