from sqlalchemy.orm import Session

from db.crud.nomination_event_judge.nomination_event_judge import create_nomination_event_judge_db, \
    get_nomination_event_judge_db, delete_nomination_event_judge_db, user_in_judge_team_db
from db.models.nomination_event import NominationEvent
from db.models.user import User
from db.schemas.user.user import UserSchema
from managers.user import UserManager


class NominationEventJudgeManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__user_manager = UserManager(db)

        self.__judge_not_found_in_judges_team_error = "judge not found in judges team error"

    def create(
            self,
            nomination_event_db: type(NominationEvent),
            judge_db: type(User)
    ):
        create_nomination_event_judge_db(self.__db, nomination_event_db, judge_db)

    def list(
            self,
            nomination_event_db: type(NominationEvent),
    ):
        judges_db = get_nomination_event_judge_db(nomination_event_db)
        judges = [UserSchema.from_orm(judge_db) for judge_db in judges_db]
        return judges

    def delete(
            self,
            nomination_event_db: type(NominationEvent),
            judge_db: type(User)
    ):
        delete_nomination_event_judge_db(self.__db, nomination_event_db, judge_db)

    def raise_exception_if_user_not_in_judge_team(self, nomination_event_db: NominationEvent, user: User):
        user_in_judge_team = user_in_judge_team_db(nomination_event_db, user)
        return user_in_judge_team
