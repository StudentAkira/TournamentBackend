from fastapi import Cookie, HTTPException
from starlette import status
from typing_extensions import Annotated

from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authorized_only(token: Annotated[str | None, Cookie()] = None):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "logged out"}
        )
    return token
