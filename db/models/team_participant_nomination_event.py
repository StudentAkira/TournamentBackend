from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class TeamParticipantNominationEvent(Base):
    __tablename__ = "team_participant_nomination_event"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_participant_id: Mapped["int"] = mapped_column(ForeignKey("team_participant.id"))
    nomination_event_id: Mapped["int"] = mapped_column(ForeignKey("nomination_event.id"))

    equipment = Column(String)
    software = Column(String)
