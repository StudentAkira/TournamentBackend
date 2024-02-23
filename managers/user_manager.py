from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from db.crud import pwd_context, get_user_by_id_db, create_user_db, get_user_by_email_db
from db.schemas import UserRole, DatabaseUser, CreateUser


class UserManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__wrong_secret_error = "wrong secret"
        self.__email_taken_error = "email taken"
        self.__secret_missing_error = "secret missing"
        self.__invalid_role_error = "invalid role"
        self.__invalid_password_error = "invalid password"
        self.__user_not_found_error = "user not found"
        self.__access_denied_error = "you are not allowed to perform this action"
        self.__educational_institution_is_none_error = "educational institution cannot be none for non judge user"

    def get_user_by_id(self, user_id: int) -> DatabaseUser:
        db_user = get_user_by_id_db(self.__db, user_id)
        self.raise_exception_if_user_not_found(db_user)
        return db_user

    def get_user_by_email(self, email: str) -> DatabaseUser:
        db_user = get_user_by_email_db(self.__db, email)
        self.raise_exception_if_user_not_found(db_user)
        return db_user

    def create_user(self, user: CreateUser):
        self.raise_exception_if_email_taken(user.email)
        self.raise_exception_if_user_not_judge_and_educational_institution_is_none(user)
        create_user_db(self.__db, user)

    def check_user_password(self, user: DatabaseUser, password: str):
        password_correct = pwd_context.verify(password, user.hashed_password)
        self.raise_exception_if_password_incorrect(password_correct)

    def raise_exception_if_email_taken(self, email: EmailStr):
        db_user = get_user_by_email_db(self.__db, email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__email_taken_error}
            )

    def raise_exception_if_password_incorrect(self, correct: bool):
        if not correct:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": self.__invalid_password_error}
            )

    def raise_exception_if_user_not_found(self, user: DatabaseUser):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": self.__user_not_found_error}
            )

    def raise_exception_if_user_is_not_admin(self, role: str):
        if role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__access_denied_error}
            )

    def raise_exception_if_user_is_not_judge(self, user: CreateUser):
        if user.role != UserRole.judge:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__access_denied_error}
            )

    def raise_exception_if_user_not_judge_and_educational_institution_is_none(self, user: CreateUser):
        if user.role != UserRole.judge and user.educational_institution is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__educational_institution_is_none_error}
            )