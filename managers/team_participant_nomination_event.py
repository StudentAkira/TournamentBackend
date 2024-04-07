from pydantic import EmailStr
from sqlalchemy.orm import Session

from db.crud.team_participant_nomination_event.team_participant_nomination_event import \
    append_team_participant_nomination_event_db, update_team_participant_nomination_event_db, \
    delete_team_participant_nomination_event_db
from db.schemas.team_nomination_event.append_team_participant_nomination_event import \
    AppendTeamParticipantNominationEventSchema
from db.schemas.team_nomination_event.delete_team_participant_nomination_event import \
    DeleteTeamParticipantNominationEventSchema
from db.schemas.team_nomination_event.update_team_participant_nomination_event import \
    UpdateTeamParticipantNominationEventSchema


class TeamParticipantNominationEventManager:
    __db: Session

    def __init__(self, db: Session):
        self.__db = db

    def append_team_participant_nomination_event(
            self,
            team_participant_nomination_event_data: AppendTeamParticipantNominationEventSchema
    ):
        append_team_participant_nomination_event_db(self.__db, team_participant_nomination_event_data)

    def update_team_participant_nomination_event(
            self,
            team_participant_nomination_event_data: UpdateTeamParticipantNominationEventSchema
    ):
        update_team_participant_nomination_event_db(self.__db, team_participant_nomination_event_data)

    def delete_team_participant_nomination_event(
            self,
            team_participant_nomination_event_data: DeleteTeamParticipantNominationEventSchema
    ):
        delete_team_participant_nomination_event_db(self.__db, team_participant_nomination_event_data)
