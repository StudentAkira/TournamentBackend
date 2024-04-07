from typing import cast

from sqlalchemy.orm import Session

from db.models.token import Token
from db.schemas.token.token_database import TokenDatabaseSchema


def save_token_db(db: Session, token: str, user_id: int) -> TokenDatabaseSchema:
    token_db = Token(
        token=token,
        owner_id=user_id
    )
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return token_db


def delete_token_db(db: Session, token: str):
    db_token = db.query(Token).filter(
        cast("ColumnElement[bool]", Token.token == token)
    ).first()
    if db_token:
        db.query(Token).filter(
            cast("ColumnElement[bool]", Token.token == token)
        ).delete()
    db.commit()


def get_token_db(db: Session, token: str) -> type(Token):
    token_db = db.query(Token).filter(
        cast("ColumnElement[bool]", Token.token == token)
    ).first()
    return token_db
