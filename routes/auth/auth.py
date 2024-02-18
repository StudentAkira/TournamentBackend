from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from db.schemas import UserCreate, UserLogin
from dependencies import get_db
from routes.auth.auth_service import AuthService

auth = APIRouter(prefix="/auth")


@auth.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(user)


@auth.post("/logout")
async def logout(token: Annotated[str, Body()], db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.logout()


@auth.post("/sign_in")
async def sign_in(user: UserCreate, secret: Annotated[str | None, Body()], db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.sign_in(user, secret)
