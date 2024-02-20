from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from db.schemas import LoginUser
from dependencies import get_db
from routes.auth.auth_service import AuthService

auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/login")
async def login(user: LoginUser, db: Session = Depends(get_db)) -> dict[str, str]:
    service = AuthService(db)
    return service.login(user)


@auth.post("/logout")
async def logout(token: Annotated[str, Body()], db: Session = Depends(get_db)) -> dict[str, str]:
    service = AuthService(db)
    return service.logout(token)
