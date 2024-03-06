from db.schemas.token import TokenDecodedSchema
from db.schemas.user import UserRole
from managers.event_manager import EventManager
from managers.nomination_event_manager import NominationEventManager
from managers.nomination_manager import NominationManager
from managers.team_manager import TeamManager


class Validator:
    def __init__(self, db):
        self.__nomination_event_manager = NominationEventManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__event_manager = EventManager(db)
        self.__team_manager = TeamManager(db)
        self.__db = db

    def check_team_event_nomination__nomination_event__existence(self,
                                                                 team_name: str,
                                                                 nomination_name: str,
                                                                 event_name: str
                                                                 ):
        self.__team_manager.raise_exception_if_team_not_found(team_name)
        self.__event_manager.raise_exception_if_event_not_found(event_name)
        self.__nomination_manager.raise_exception_if_nomination_not_found(nomination_name)
        self.__nomination_event_manager.raise_exception_if_nomination_event_not_found(nomination_name, event_name)

    def check_if_team_not_in_event_nomination(
            self,
            team_name,
            nomination_name,
            event_name
    ):
        self.__nomination_event_manager.raise_exception_if_team_not_in_event_nomination(
            team_name,
            nomination_name,
            event_name
        )

    def check_participant_team_relation_existence(self, team_name: str, nomination_name: str, event_name: str):
        self.__nomination_event_manager.raise_exception_if_team_already_in_nomination_event(
            team_name,
            nomination_name,
            event_name
        )
        self.__nomination_event_manager.raise_exception_if_participant_already_in_nomination_event(
            team_name,
            nomination_name,
            event_name
        )

    def validate_user_entity_ownership(self, decoded_token: TokenDecodedSchema, team_name: str, event_name: str):
        if decoded_token.role == UserRole.specialist or decoded_token.role == UserRole.judge:
            self.__team_manager.raise_exception_if_team_owner_wrong(team_name, decoded_token.user_id)
        if decoded_token.role == UserRole.judge:
            self.__event_manager.raise_exception_if_event_owner_wrong(event_name, decoded_token.user_id)
