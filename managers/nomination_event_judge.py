from sqlalchemy.orm import Session

from db.crud.nomination_event_judge.nomination_event_judge import create_nomination_event_judge_db, \
    get_nomination_event_judge_db, delete_nomination_event_judge_db
from db.schemas.nomination_event_judge.get_nomination_event_judge import GenNominationEventJudgeSchema
from db.schemas.nomination_event_judge.nomination_event_judge_data import NominationEventJudgeDataSchema
from db.schemas.user.user import UserSchema


class NominationEventJudgeManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

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
