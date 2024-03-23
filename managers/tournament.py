from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.nomination_event import close_registration_nomination_event_db
from db.crud.tournaments import create_group_tournament_db, \
    get_groups_of_tournament_db, get_count_of_participants_of_tournament_db
from db.schemas.group_tournament import StartGroupTournamentSchema
from db.schemas.nomination_event import NominationEventSchema


class TournamentManager:
    __db: Session

    def __init__(self, db):
        self.__db = db
        self.__invalid_group_count_error = "invalid group count"

    def create_group_tournament(self, nomination_event: StartGroupTournamentSchema):
        close_registration_nomination_event_db(self.__db, NominationEventSchema(
            **nomination_event.model_dump()
        ))
        self.validate_group_count(
            nomination_event.group_count,
            nomination_event.nomination_name,
            nomination_event.event_name,
            nomination_event.type
        )
        create_group_tournament_db(self.__db, nomination_event)

    def get_groups_of_tournament(self, nomination_event: NominationEventSchema):
        return get_groups_of_tournament_db(self.__db, nomination_event)

    def validate_group_count(self, group_count: int, nomination_name: str, event_name: str, nomination_event_type: str):
        team_count = get_count_of_participants_of_tournament_db(
            self.__db,
            nomination_name,
            event_name,
            nomination_event_type
        )
        max_group_amount = int(team_count / 2)
        if team_count <= 3 and group_count >= 2:
            self.raise_exception_if_group_count_wrong()
        if group_count > team_count:
            self.raise_exception_if_group_count_wrong()
        if group_count > max_group_amount:
            self.raise_exception_if_group_count_wrong()

    def raise_exception_if_group_count_wrong(self):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": self.__invalid_group_count_error}
        )
