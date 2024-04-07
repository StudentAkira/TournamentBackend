from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.nomination_event_judge.nomination_event_judge import create_nomination_event_judge_db, \
    get_nomination_event_judge_db, delete_nomination_event_judge_db
from db.schemas.nomination_event_judge.get_nomination_event_judge import GenNominationEventJudgeSchema
from db.schemas.nomination_event_judge.nomination_event_judge_data import NominationEventJudgeDataSchema
from db.schemas.user.user import UserSchema
from managers.user import UserManager


class NominationEventJudgeManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__user_manager = UserManager(db)

        self.__judge_not_found_in_judges_command_error = "judge not found in judges command error"

    def create(
            self,
            nomination_event_judge_data: NominationEventJudgeDataSchema
    ):
        create_nomination_event_judge_db(self.__db, nomination_event_judge_data)

    def list(
            self,
            nomination_event_judge_data: GenNominationEventJudgeSchema
    ):
        judges_db = get_nomination_event_judge_db(self.__db, nomination_event_judge_data)
        judges = [UserSchema.from_orm(judge_db) for judge_db in judges_db]
        return judges

    def delete(
            self,
            nomination_event_judge_data: NominationEventJudgeDataSchema
    ):
        delete_nomination_event_judge_db(self.__db, nomination_event_judge_data)

    def raise_exception_if_judge_not_in_judge_command(
            self,
            nomination_event_judge_data: NominationEventJudgeDataSchema
    ):
        judges = get_nomination_event_judge_db(
            self.__db,
            GenNominationEventJudgeSchema(**nomination_event_judge_data.model_dump())
        )
        judge = self.__user_manager.get_user_by_email(nomination_event_judge_data.email)

        if judge.email not in set(judge.email for judge in judges):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__judge_not_found_in_judges_command_error}
            )
