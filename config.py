from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_secret_key: str = "supersecret"

    jwt_token_secret: str = "supersecret"
    jwt_algorithm: str = "supersecret"
    jwt_token_expiration_time_days: int = 2

    db: str = "supersecret"
    db_name: str = "supersecret"
    db_user: str = "supersecret"
    db_password: str = "supersecret"
    db_host: str = "supersecret"

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()


