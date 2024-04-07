from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event_judge.get_nomination_event_judge import GenNominationEventJudgeSchema
from db.schemas.nomination_event_judge.nomination_event_judge_data import NominationEventJudgeDataSchema
from managers.event import EventManager
from managers.nomination import NominationManager
from managers.nomination_event import NominationEventManager
from managers.nomination_event_judge import NominationEventJudgeManager
from managers.token import TokenManager
from managers.user import UserManager
from utils.validation_util import Validator


class NominationEventJudgeService:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__token_manager = TokenManager(db)
        self.__nomination_event_judge_manager = NominationEventJudgeManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__event_manager = EventManager(db)
        self.__nomination_event_manager = NominationEventManager(db)
        self.__user_manager = UserManager(db)
        self.__nomination_event_judge_manager = NominationEventJudgeManager(db)
        self.__validator = Validator(db)

        self.__judge_appended_message = "judge appended"
        self.__judge_deleted_message = "judge deleted"

    def append_judge_to_nomination_event(
            self,
            response: Response,
            token: str,
            nomination_event_judge_data: NominationEventJudgeDataSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        self.__validator.check_event_nomination__nomination_event_existence(
            nomination_event_judge_data.nomination_name,
            nomination_event_judge_data.event_name,
            nomination_event_judge_data.nomination_event_type
        )
        self.__event_manager.raise_exception_if_owner_wrong(
            nomination_event_judge_data.event_name,
            decoded_token.user_id
        )
        self.__user_manager.raise_exception_if_user_not_found(nomination_event_judge_data)
        self.__user_manager.raise_exception_if_user_specialist(nomination_event_judge_data.email)
        judge = self.__user_manager.get_user_by_email(nomination_event_judge_data.email)
        self.__user_manager.raise_exception_if_user_specialist(judge.role)
        self.__validator.raise_exception_if_registration_finished(
            nomination_event_judge_data.nomination_name,
            nomination_event_judge_data.event_name,
            nomination_event_judge_data.nomination_event_type
        )
        self.__nomination_event_judge_manager.create(nomination_event_judge_data)
        return {"message": self.__judge_appended_message}

    def get_nomination_event_judges(
            self,
            response: Response,
            token: str,
            nomination_event_judge_data: GenNominationEventJudgeSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        self.__validator.check_event_nomination__nomination_event_existence(
            nomination_event_judge_data.nomination_name,
            nomination_event_judge_data.event_name,
            nomination_event_judge_data.nomination_event_type
        )
        self.__event_manager.raise_exception_if_owner_wrong(
            nomination_event_judge_data.event_name,
            decoded_token.user_id
        )
        return self.__nomination_event_judge_manager.list(nomination_event_judge_data)

    def delete_judge_from_nomination_event(
            self,
            response: Response,
            token: str,
            nomination_event_judge_data: NominationEventJudgeDataSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        self.__validator.check_event_nomination__nomination_event_existence(
            nomination_event_judge_data.nomination_name,
            nomination_event_judge_data.event_name,
            nomination_event_judge_data.nomination_event_type
        )
        self.__event_manager.raise_exception_if_owner_wrong(
            nomination_event_judge_data.event_name,
            decoded_token.user_id
        )
        self.__validator.raise_exception_if_registration_finished(
            nomination_event_judge_data.nomination_name,
            nomination_event_judge_data.event_name,
            nomination_event_judge_data.nomination_event_type
        )
        self.__user_manager.raise_exception_if_user_not_found(nomination_event_judge_data)
        self.__nomination_event_judge_manager.delete(nomination_event_judge_data)
        return {"message": self.__judge_deleted_message}
