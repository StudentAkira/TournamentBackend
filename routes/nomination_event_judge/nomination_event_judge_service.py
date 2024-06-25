from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event_judge.get_nomination_event_judge import GetNominationEventJudgeSchema
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
            nomination_event_judge: NominationEventJudgeDataSchema
    ):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.get_decoded_token_user_event_nomination_nomination_event(response, token, nomination_event_judge)
        self.__event_manager.raise_exception_if_owner_wrong(
            event_db,
            decoded_token.user_id
        )
        self.__user_manager.raise_exception_if_user_specialist(user_db.role)
        judge_db = self.__user_manager.get_user_by_id_or_raise_if_not_found(nomination_event_judge.judge_id)
        self.__user_manager.raise_exception_if_user_specialist(judge_db.role)
        self.__nomination_event_manager.raise_exception_if_registration_finished(nomination_event_db)
        self.__nomination_event_judge_manager.create(
            nomination_event_db,
            judge_db
        )
        return {"message": self.__judge_appended_message}

    def get_nomination_event_judges(
            self,
            response: Response,
            token: str,
            nomination_event_judge: GetNominationEventJudgeSchema
    ):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.get_decoded_token_user_event_nomination_nomination_event(response, token, nomination_event_judge)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        self.__nomination_event_manager.raise_exception_if_user_not_in_judge_command(
            nomination_event_db,
            user_db
        )
        return self.__nomination_event_judge_manager.list(nomination_event_db)

    def delete_judge_from_nomination_event(
            self,
            response: Response,
            token: str,
            nomination_event_judge: NominationEventJudgeDataSchema
    ):
        decoded_token, user_db, event_db, nomination_db, nomination_event_db = \
            self.get_decoded_token_user_event_nomination_nomination_event(response, token, nomination_event_judge)
        self.__nomination_event_manager.raise_exception_if_registration_finished(nomination_event_db)
        judge_db = self.__user_manager.get_user_by_id_or_raise_if_not_found(nomination_event_judge.judge_id)
        self.__event_manager.raise_exception_if_owner_wrong(event_db, user_db.id)
        self.__nomination_event_judge_manager.delete(nomination_event_db, judge_db)
        return {"message": self.__judge_deleted_message}

    def get_decoded_token_user_event_nomination_nomination_event(
            self,
            response: Response,
            token: str,
            nomination_event_judge:
            NominationEventJudgeDataSchema | GetNominationEventJudgeSchema
    ):
        decoded_token = self.__token_manager.decode_token(token, response)
        self.__user_manager.raise_exception_if_user_specialist(decoded_token.role)
        user_db = self.__user_manager.get_user_by_id_or_raise_if_not_found(decoded_token.user_id)
        event_db = self.__event_manager.get_by_id_or_raise_if_not_found(
            nomination_event_judge.event_id
        )
        nomination_db = self.__nomination_manager.get_by_id_and_user_id_or_raise_exception_if_not_found(
            decoded_token.user_id,
            nomination_event_judge.nomination_id
        )
        nomination_event_db = self.__nomination_event_manager.get_nomination_event_or_raise_if_not_found(
            nomination_db,
            event_db,
            nomination_event_judge.nomination_event_type
        )
        return decoded_token, user_db, event_db, nomination_db, nomination_event_db
