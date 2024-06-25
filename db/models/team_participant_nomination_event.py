from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

if TYPE_CHECKING:
    from db.models.software import Software
    from db.models.equipment import Equipment


class TeamParticipantNominationEvent(Base):
    __tablename__ = "team_participant_nomination_event"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_participant_id: Mapped["int"] = mapped_column(ForeignKey("team_participant.id"))
    nomination_event_id: Mapped["int"] = mapped_column(ForeignKey("nomination_event.id"))

    softwares: Mapped[list["Software"]] = \
        relationship(
            "Software",
            back_populates="team_participants_nomination_events",
            secondary="team_participants_nomination_event_software",
            cascade="all,delete",
        )
    equipments: Mapped[list["Equipment"]] = \
        relationship(
            "Equipment",
            back_populates="team_participants_nomination_events",
            secondary="team_participants_nomination_event_equipment",
            cascade="all,delete",
        )
