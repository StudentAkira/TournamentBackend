import secrets

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from config import settings
from db.crud import get_user_by_username_db, pwd_context, get_user_by_id_db, create_user_db
from db.schemas import UserCreate, UserDB, UserRole


class UserManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__wrong_secret_error = "wrong secret"
        self.__username_taken_error = "username taken"
        self.__secret_missing_error = "secret missing"
        self.__invalid_role_error = "invalid role"
        self.__invalid_password_error = "invalid password"
        self.__user_not_found_error = "user not found"
        self.__user_is_not_admin_error = "you are not performed to to this action"
        self.__user_is_not_judge_error = "you are not performed to to this action"

    def get_user_by_id(self, user_id: int) -> UserDB:
        db_user = get_user_by_id_db(self.__db, user_id)
        self.raise_exception_if_user_not_found(db_user)
        return db_user

    def get_user_by_username(self, username: str):
        db_user = get_user_by_username_db(self.__db, username)
        self.raise_exception_if_user_not_found(db_user)
        return db_user

    def create_user(self, user: UserCreate):
        self.raise_exception_if_username_taken(user.username)
        create_user_db(self.__db, user)

    def create_judge(self, user: UserCreate):
        self.create_user(user)

    def create_admin(self, user: UserCreate, secret: str):
        self.check_secret_for_superuser_creation(secret)
        self.create_user(user)

    def check_secret_for_superuser_creation(self, secret: str):
        match = secrets.compare_digest(secret, settings.app_secret_key)
        if not match:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": self.__wrong_secret_error}
            )

    def check_user_password(self, user: UserDB, password: str):
        password_correct = pwd_context.verify(password, user.hashed_password)
        self.raise_exception_if_password_incorrect(password_correct)

    def raise_exception_if_username_taken(self, username: str):
        db_user = get_user_by_username_db(self.__db, username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__username_taken_error}
            )

    def raise_exception_if_password_incorrect(self, correct: bool):
        if not correct:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": self.__invalid_password_error}
            )

    def raise_exception_if_user_not_found(self, user: UserDB):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": self.__user_not_found_error}
            )

    def raise_exception_if_user_is_not_admin(self, user):
        if user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__user_is_not_admin_error}
            )

    def raise_exception_if_user_is_not_judge(self, user):
        if user.role != UserRole.judge:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__user_is_not_judge_error}
            )

