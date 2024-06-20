from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.crud.team_participant_nomination_event.team_participant_nomination_event import \
    append_team_participant_nomination_event_db, update_team_participant_nomination_event_db, \
    delete_team_participant_nomination_event_db, refresh_db
from db.models.nomination_event import NominationEvent
from db.models.participant import Participant
from db.models.user import User
from db.schemas.team_nomination_event.append_team_participant_nomination_event import \
    AppendTeamParticipantNominationEventSchema
from db.schemas.team_nomination_event.update_team_participant_nomination_event import \
    UpdateTeamParticipantNominationEventSchema
from db.schemas.team_participant_nomination_event.append_teams_participants_nomination_event import \
    TeamParticipantNominationEventAppendSchema
from db.schemas.user.user_role import UserRole
from managers.nomination_event import NominationEventManager
from managers.participant import ParticipantManager
from managers.team import TeamManager
from managers.team_participant import TeamParticipantManager


class TeamParticipantNominationEventManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

        self.__participant_manager = ParticipantManager(db)
        self.__team_manager = TeamManager(db)
        self.__team_participant_manager = TeamParticipantManager(db)
        self.__nomination_event_manger = NominationEventManager(db)

        self.__team_present_more_then_one_time = "team present more then one time"
        self.__participant_present_more_then_one_time = "participant present more then one time"

    def append_team_participant_nomination_event(
            self,
            nomination_event_db: type(NominationEvent),
            participant_db: type(Participant),
            team_db: type(Participant),
            team_participant_nomination_event: AppendTeamParticipantNominationEventSchema
    ):
        append_team_participant_nomination_event_db(
            self.__db,
            nomination_event_db,
            team_db,
            participant_db,
            team_participant_nomination_event
        )

    def update_team_participant_nomination_event(
            self,
            nomination_event_db: type(NominationEvent),
            participant_db: type(Participant),
            team_participant_nomination_event: UpdateTeamParticipantNominationEventSchema
    ):
        update_team_participant_nomination_event_db(
            self.__db,
            nomination_event_db,
            participant_db,
            team_participant_nomination_event
        )

    def delete_team_participant_nomination_event(
            self,
            nomination_event_db: type(NominationEvent),
            participant_db: type(Participant),
    ):
        delete_team_participant_nomination_event_db(self.__db, nomination_event_db, participant_db)

    def refresh(
            self,
            team_participant_nomination_event: TeamParticipantNominationEventAppendSchema,
            nomination_event_db: NominationEvent
    ):
        refresh_db(self.__db, nomination_event_db, team_participant_nomination_event)

    def validate_received_schema(
            self,
            team_participant_nomination_event: TeamParticipantNominationEventAppendSchema,
            nomination_event_db: NominationEvent,
            user_db: User
    ):
        participant_ids = [tp.participant_id for tp in team_participant_nomination_event.team_participants]

        team_db = self.__team_manager.get_by_id(team_participant_nomination_event.team_id)
        self.__team_manager.raise_exception_if_not_found(team_db)

        self.raise_exception_if_participant_present_more_then_one_time(participant_ids)
        if user_db.role != UserRole.admin:
            self.__team_manager.raise_exception_if_owner_wrong(team_db, user_db)

        for tp in team_participant_nomination_event.team_participants:
            participant_db = self.__participant_manager.get_by_id(tp.participant_id)
            self.__participant_manager.raise_exception_if_not_found(participant_db)
            if user_db.role != UserRole.admin:
                self.__participant_manager.raise_exception_if_owner_wrong(participant_db, user_db)
            self.__team_participant_manager.raise_exception_if_participant_not_in_team(participant_db, team_db)
            self.__nomination_event_manger.raise_exception_if_participant_in_nomination_event(
                participant_db,
                nomination_event_db
            )

    def raise_exception_if_participant_present_more_then_one_time(self, participant_ids: list[int]):
        if len(participant_ids) != len(set(participant_ids)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_present_more_then_one_time}
            )


