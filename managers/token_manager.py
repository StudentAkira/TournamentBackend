import datetime
import time

import jwt
from fastapi import HTTPException
from jwt import DecodeError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from config import settings
from db.crud.token import save_token_db, delete_token_db, get_token_db
from db.schemas.token import TokenDecodedSchema


class TokenManager:

    def __init__(self, db: Session):
        self.__db = db

        self.__jwt_token_expiration_time = settings.jwt_token_expiration_time_days
        self.__jwt_token_secret = settings.jwt_token_secret
        self.__jwt_algorithm = settings.jwt_algorithm

        self.__token_expired_error = "Token expired, you are currently logged out"
        self.__token_signature_error = "Token signature error, invalid token"
        self.__token_not_found_error = "Token does not exist"
        self.__invalid_token_error = "Token is invalid"

    def save_token_db(self, token: str, user_id: int):
        save_token_db(self.__db, token, user_id)

    def delete_token_from_db(self, token: str):
        delete_token_db(self.__db, token)

    def check_if_token_exists_in_db(self, token: str):
        db_token = get_token_db(self.__db, token)
        self.raise_exception_if_token_not_found(db_token)

    def generate_token(self, user_id: int, role: str) -> str:
        to_encode = {
            "user_id": user_id,
            "role": role,
            "exp":
                datetime.datetime.now(tz=datetime.timezone.utc) +
                datetime.timedelta(days=self.__jwt_token_expiration_time),
            "milliseconds": (round(time.time() * 1000) % 1000)
        }
        token = jwt.encode(payload=to_encode, key=self.__jwt_token_secret, algorithm=self.__jwt_algorithm)
        self.save_token_db(token, user_id)
        return token

    def decode_token(self, token, response: Response) -> TokenDecodedSchema:
        try:
            decoded = jwt.decode(
                token,
                key=self.__jwt_token_secret,
                algorithms=[self.__jwt_algorithm]
            )
        except jwt.InvalidSignatureError:
            response.delete_cookie(key="token")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": self.__token_signature_error}
            )
        except DecodeError:
            response.delete_cookie(key="token")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": self.__invalid_token_error}
            )
        except jwt.ExpiredSignatureError:
            response.delete_cookie(key="token")
            self.delete_token_db(token)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": self.__token_expired_error}
            )
        decoded = TokenDecodedSchema(**decoded)
        return decoded

    def raise_exception_if_token_not_found(self, token):
        if not token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__token_not_found_error}
            )
