from fastapi import APIRouter, Path, Depends, Body, Cookie
from sqlalchemy.orm import Session
from starlette.responses import Response
from typing_extensions import Annotated

from db.crud import create_user_db
from db.schemas import BaseUser, CreateUser, UserRole
from dependencies import get_db, authorized_only
from routes.users.users_service import UsersService

users = APIRouter(prefix="/users", tags=["users"])


@users.get("/get_my_profile/")
async def get_my_profile(response: Response, token: str = Depends(authorized_only), db: Session = Depends(get_db)) -> BaseUser:
    service = UsersService(db)
    return service.get_user_data(response, token)


@users.get('/create_superadmin')
async def create_super_admin(db: Session = Depends(get_db)):
    user = CreateUser(
        email="test@mail.ru",
        password="7689462",
        first_name="Akira",
        second_name="Akira",
        third_name="Akira",
        phone="+375297777777",
        educational_institution=None,
        region="Akira",
        role=UserRole.admin,
    )
    create_user_db(db, user)
    return {"message": "admin created"}


@users.post("/create_user")
async def create_user(response: Response, user: CreateUser, token: str = Depends(authorized_only), db: Session = Depends(get_db)):
    service = UsersService(db)
    return service.create_user(response, user, token)


