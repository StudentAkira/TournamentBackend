from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.crud.user.user import create_user_db
from db.schemas.user.edit_user import EditUserSchema
from db.schemas.user.user import UserSchema
from db.schemas.user.user_create import UserCreateSchema
from db.schemas.user.user_role import UserRole
from dependencies import get_db, authorized_only
from routes.user.users_service import UsersService
from urls import URLs

users = APIRouter(prefix=URLs.user_prefix.value, tags=URLs.user_tags.value)


@users.get(URLs.profile.value)
async def get_my_profile(
        response: Response,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> UserSchema:
    service = UsersService(db)
    return service.get_user_data(response, token)


@users.get(URLs.users.value)
async def list_users(
        response: Response,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = UsersService(db)
    return service.list(response, token)


@users.patch(URLs.profile.value)
async def edit_profile(
        response: Response,
        user_data: EditUserSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)):
    service = UsersService(db)
    return service.edit_user_data(response, token, user_data)


@users.get(URLs.create_admin.value)
async def create_super_admin(db: Session = Depends(get_db)):
    user = UserCreateSchema(
        email="test@mail.ru",
        password="7689462",
        first_name="Akira",
        second_name="Akira",
        third_name="Akira",
        phone="+375-29-777-77-77",
        educational_institution=None,
        region="Akira",
        role=UserRole.admin,
    )
    create_user_db(db, user)
    return {"message": "admin created"}


@users.post(URLs.create_user.value)
async def create_user(
        response: Response,
        user: UserCreateSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = UsersService(db)
    return service.create_user(response, user, token)
