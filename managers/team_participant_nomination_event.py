from sqlalchemy.orm import Session

from db.crud.team_participant_nomination_event.team_participant_nomination_event import \
    append_team_participant_nomination_event_db, update_team_participant_nomination_event_db, \
    delete_team_participant_nomination_event_db
from db.models.nomination_event import NominationEvent
from db.models.participant import Participant
from db.schemas.team_nomination_event.append_team_participant_nomination_event import \
    AppendTeamParticipantNominationEventSchema
from db.schemas.team_nomination_event.update_team_participant_nomination_event import \
    UpdateTeamParticipantNominationEventSchema


class TeamParticipantNominationEventManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

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
