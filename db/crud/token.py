from typing import cast

from sqlalchemy.orm import Session

from db import models
from db.schemas.token import TokenDatabaseSchema


def save_token_db(db: Session, token: str, user_id: int) -> TokenDatabaseSchema:
    token_db = models.Token(
        token=token,
        owner_id=user_id
    )
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return token_db


def delete_token_db(db: Session, token: str):
    db_token = db.query(models.Token).filter(
        cast("ColumnElement[bool]", models.Token.token == token)
    ).first()
    if db_token:
        db.query(models.Token).filter(
            cast("ColumnElement[bool]", models.Token.token == token)
        ).delete()
    db.commit()


def get_token_db(db: Session, token: str) -> type(models.Token):
    token_db = db.query(models.Token).filter(
        cast("ColumnElement[bool]", models.Token.token == token)
    ).first()
    return token_db
