from typing import cast

from fastapi import HTTPException
from sqlalchemy import exists
from sqlalchemy.orm import Session
from starlette import status

from db.crud.user.user import get_users_db, get_user_by_id_db, get_user_by_email_db, create_user_db, pwd_context, \
    edit_user_data_db
from db.models.user import User
from db.schemas.nomination_event_judge.nomination_event_judge_data import NominationEventJudgeDataSchema
from db.schemas.user.edit_user import EditUserSchema
from db.schemas.user.user import UserSchema
from db.schemas.user.user_create import UserCreateSchema
from db.schemas.user.user_role import UserRole


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

    def list(self):
        users_db = get_users_db(self.__db)
        users = [UserSchema.from_orm(user_db) for user_db in users_db]
        return users

    def get_user_by_id(self, user_id: int) -> UserSchema | None:
        user_db = get_user_by_id_db(self.__db, user_id)
        if user_db:
            return UserSchema.from_orm(user_db)

    def get_user_by_email(self, email: str) -> UserSchema | None:
        user_db = get_user_by_email_db(self.__db, email)
        if user_db:
            return UserSchema.from_orm(user_db)

    def get_user_id_associated_with_email(self, user: UserSchema) -> int:
        user_db = get_user_by_email_db(self.__db, user.email)
        return user_db.id

    def create_user(self, user: UserCreateSchema):
        self.raise_exception_if_email_taken(user)
        create_user_db(self.__db, user)

    def check_user_password(self, user: UserSchema, password: str):
        user_db = get_user_by_email_db(self.__db, user.email)
        password_check = pwd_context.verify(password, user_db.hashed_password)
        self.raise_exception_if_password_incorrect(password_check)

    def edit_user_data(self, user_data: EditUserSchema, user_id: int):
        if self.get_user_by_id(user_id).email != user_data.email:
            self.raise_exception_if_email_taken(user_data)
        edit_user_data_db(self.__db, user_data, user_id)

    def raise_exception_if_email_taken(self, user: UserSchema | EditUserSchema):
        user_db = get_user_by_email_db(self.__db, user.email)
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

    def raise_exception_if_user_not_found(
            self,
            user:
                UserSchema |
                NominationEventJudgeDataSchema
    ):
        user_exists = self.__db.query(
            exists(

            ).where(
                cast("ColumnElement[bool]", User.email == user.email)
            )
        ).scalar()
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__user_not_found_error}
            )

    def raise_exception_if_user_is_not_admin(self, role: str):
        if role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__access_denied_error}
            )

    def raise_exception_if_user_is_not_judge(self, user: UserSchema):
        if user.role != UserRole.judge:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__access_denied_error}
            )

    def raise_exception_if_user_specialist(self, role: str):
        if role == UserRole.specialist:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": self.__access_denied_error}
            )
