from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.database import Base


if TYPE_CHECKING:
    from db.models.nomination_event import NominationEvent
    from db.models.match import Match


class TeamParticipant(Base):
    __tablename__ = "team_participant"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    participant_id: Mapped[int] = mapped_column(ForeignKey("participant.id"))

    nomination_events: Mapped[list["NominationEvent"]] = relationship(
        "NominationEvent",
        back_populates="team_participants",
        secondary="team_participant_nomination_event"
    )

    __table_args__ = (UniqueConstraint('team_id', 'participant_id', name='_team_id__participant_id'),)
