from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from db.database import Base


if TYPE_CHECKING:
    from db.models.team_participant_nomination_event import TeamParticipantNominationEvent


class Equipment(Base):
    __tablename__ = "equipment"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    equipment = Column(String, unique=True)

    team_participants_nomination_events: Mapped[list["TeamParticipantNominationEvent"]] =\
        relationship(
            "TeamParticipantNominationEvent",
            back_populates="equipments",
            secondary="team_participants_nomination_event_equipment"
        )
