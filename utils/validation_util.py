from db.models.event import Event
from db.models.team import Team
from db.schemas.token.token_decoded import TokenDecodedSchema
from db.schemas.user.user_role import UserRole
from managers.event import EventManager
from managers.team import TeamManager


class Validator:
    def __init__(self, db):

        self.__event_manager = EventManager(db)
        self.__team_manager = TeamManager(db)
        self.__db = db

    def validate_user_entity_ownership(
            self,
            decoded_token: TokenDecodedSchema,
            team_db: type(Team),
            event_db: type(Event)
    ):
        if decoded_token.role == UserRole.specialist or decoded_token.role == UserRole.judge:
            self.__team_manager.raise_exception_if_owner_wrong(team_db, decoded_token.user_id)
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_owner_wrong(event_db, decoded_token.user_id)
