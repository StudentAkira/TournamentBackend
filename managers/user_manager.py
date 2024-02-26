from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from db import models
from db.crud.user import get_user_by_id_db, get_user_by_email_db, create_user_db, pwd_context
from db.schemas.user import UserCreateSchema, UserRole, UserSchema


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

    def get_user_by_id(self, user_id: int) -> UserSchema | None:
        user_db = get_user_by_id_db(self.__db, user_id)
        if user_db:
            return UserSchema.from_orm(user_db)

    def get_user_by_email(self, email: str) -> UserSchema | None:
        user_db = self.get_db_user_by_email(email)
        if user_db:
            return UserSchema.from_orm(user_db)

    def get_db_user_by_email(self, email: str) -> models.User:
        user_db = get_user_by_email_db(self.__db, email)
        return user_db

    def create_user(self, user: UserCreateSchema):
        self.raise_exception_if_email_taken(user.email)
        create_user_db(self.__db, user)

    def check_user_password(self, user: UserSchema, password: str):
        user_db = self.get_db_user_by_email(user.email)
        password_correct = pwd_context.verify(password, user_db.hashed_password)
        self.raise_exception_if_password_incorrect(password_correct)

    def raise_exception_if_email_taken(self, email: EmailStr):
        user_db = get_user_by_email_db(self.__db, email)
        if user_db:
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

    def raise_exception_if_user_not_found(self, user: UserSchema):
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

    def raise_exception_if_user_is_not_judge(self, role: str):
        if role != UserRole.judge:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__access_denied_error}
            )

    def raise_exception_if_user_specialist(self, role):
        if role == UserRole.specialist:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__access_denied_error}
            )
