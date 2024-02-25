from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette.responses import Response
from typing_extensions import Annotated

from db.schemas import LoginUser
from dependencies import get_db, authorized_only
from routes.auth.auth_service import AuthService

auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/login")
async def login(response: Response, user: LoginUser, db: Session = Depends(get_db)) -> dict[str, str]:
    service = AuthService(db)
    return service.login(response, user)


@auth.post("/logout")
async def logout(response: Response, token: str = Depends(authorized_only), db: Session = Depends(get_db)) -> dict[str, str]:
    service = AuthService(db)
    return service.logout(response, token)
