from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from db.database import Base


class TeamParticipantNominationEventSoftware(Base):
    __tablename__ = "team_participants_nomination_event_software"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_participant_nomination_event_id: Mapped[int] =\
        mapped_column(ForeignKey("team_participant_nomination_event.id"))
    software_id: Mapped[int] = mapped_column(ForeignKey("software.id"))

    __table_args__ = (UniqueConstraint(
        'software_id',
        'team_participant_nomination_event_id',
        name='_team_participant_nomination_event_id_software_id'
    ),)
