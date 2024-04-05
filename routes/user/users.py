from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.crud.user import create_user_db
from db.schemas.user import UserSchema, UserCreateSchema, UserRole, EditUserSchema
from dependencies import get_db, authorized_only
from routes.user.users_service import UsersService

users = APIRouter(prefix="/api/user", tags=["user"])


@users.get("/profile")
async def get_my_profile(
        response: Response,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> UserSchema:
    service = UsersService(db)
    return service.get_user_data(response, token)


@users.get("/users")
async def list_users(
        response: Response,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = UsersService(db)
    return service.list(response, token)


@users.patch("/profile")
async def edit_profile(
        response: Response,
        user_data: EditUserSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)):
    service = UsersService(db)
    return service.edit_user_data(response, token, user_data)


@users.get('/create_admin')
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


@users.post("/create_user")
async def create_user(
        response: Response,
        user: UserCreateSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = UsersService(db)
    return service.create_user(response, user, token)
