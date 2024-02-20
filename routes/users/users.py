from fastapi import APIRouter, Path, Depends, Body
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from db.crud import create_user_db
from db.schemas import BaseUser, CreateUser, UserRole
from dependencies import get_db
from routes.users.users_service import UsersService

users = APIRouter(prefix="/users", tags=["users"])


@users.get("/get_my_profile/{token}")
async def get_my_profile(token: Annotated[str, Path()], db: Session = Depends(get_db)) -> BaseUser:
    service = UsersService(db)
    return service.get_user_data(token)


@users.post("/create_user")
async def create_user(token: Annotated[str, Body()], user: CreateUser,  db: Session = Depends(get_db)):
    service = UsersService(db)
    return service.create_user(user, token)


# @users.get('/create_superadmin')
# async def create_super_admin(db: Session = Depends(get_db)):
#     user = CreateUser(
#         email="test@mail.ru",
#         password="7689462",
#         first_name="Akira",
#         second_name="Akira",
#         third_name="Akira",
#         phone="+375297777777",
#         educational_institution=None,
#         region="Akira",
#         role=UserRole.admin,
#     )
#     create_user_db(db, user)
#     return {"message": "admin created"}
