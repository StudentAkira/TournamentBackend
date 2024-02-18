import secrets

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from config import settings
from db.crud import create_user, get_user_by_username, pwd_context
from db.schemas import UserCreate, UserRole, UserDB


class UserManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__wrong_secret_error = "wrong secret"
        self.__username_taken_error = "username taken"
        self.__secret_missing_error = "secret missing"
        self.__invalid_role_error = "invalid role"
        self.__invalid_password_error = "invalid password"
        self.__user_not_found_error = "user not found"

    def get_user_by_username(self, username):
        db_user = get_user_by_username(self.__db, username)
        self.raise_error_if_user_not_found(db_user)
        

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

    def check_user_password(self, user: UserDB, password: str):
        password_correct = pwd_context.verify(password, user.hashed_password)
        self.raise_exception_id_password_incorrect(password_correct)

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

    def raise_exception_id_password_incorrect(self, correct):
        if not correct:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": self.__invalid_password_error}
            )

    def raise_error_if_user_not_found(self, user):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_UNAUTHORIZED,
                detail={"error": self.__user_not_found_error}
            )
