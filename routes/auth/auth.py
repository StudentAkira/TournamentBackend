from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.user.user_login import UserLoginSchema
from dependencies.dependencies import get_db, authorized_only
from routes.auth.auth_service import AuthService
from urls import URLs


auth = APIRouter(prefix=URLs.auth_prefix.value, tags=URLs.auth_tags.value)


@auth.post(URLs.login.value)
async def login(
        response: Response,
        user: UserLoginSchema,
        db: Session = Depends(get_db)
) -> dict[str, str]:
    service = AuthService(db)
    return service.login(response, user)


@auth.post(URLs.logout.value)
async def logout(
        response: Response,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
) -> dict[str, str]:
    service = AuthService(db)
    return service.logout(response, token)
