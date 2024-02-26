from starlette.responses import Response

from db.schemas.software import SoftwareSchema
from managers.software_manager import SoftwareManager
from managers.token_manager import TokenManager


class SoftwareService:
    def __init__(self, db):
        self.__db = db

        self.__token_manager = TokenManager(db)
        self.__software_manager = SoftwareManager(db)

        self.__software_created_message = "software created"

    def create_software(self, response: Response, token: str, software: list[SoftwareSchema]):
        self.__token_manager.decode_token(token, response)
        self.__software_manager.create_software(software)
        return {"message": self.__software_created_message}

    def get_software(self, response: Response, offset: int, limit: int, token: str):
        self.__token_manager.decode_token(token, response)
        return self.__software_manager.get_softwares(offset, limit)
