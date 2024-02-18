from fastapi import APIRouter, Depends, Body, Path
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from db.schemas import UserCreate, UserLogin, UserGet
from dependencies import get_db
from routes.auth.auth_service import AuthService

auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.get("/get_my_profile/{token}")
async def my_profile(token: Annotated[str, Path()],  db: Session = Depends(get_db)) -> dict[str, UserGet]:
    service = AuthService(db)
    return service.get_user_data(token)


@auth.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)) -> dict[str, str]:
    service = AuthService(db)
    return service.login(user)


@auth.post("/logout")
async def logout(token: Annotated[str, Body()], db: Session = Depends(get_db)) -> dict[str, str]:
    service = AuthService(db)
    return service.logout(token)


@auth.post("/create_admin")
async def create_admin(user: UserCreate, secret: Annotated[str, Body()], db: Session = Depends(get_db)) -> dict[str, str]:
    service = AuthService(db)
    return service.create_admin(user, secret)


@auth.post("/create_judge")
async def create_judge(user: UserCreate, token: Annotated[str, Body()], db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.create_judge(user, token)
