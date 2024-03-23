from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.database import Base
from db.schemas.nomination_event import NominationEventType


if TYPE_CHECKING:
    from db.models.team_participant import TeamParticipant
    from db.models.user import User
    from db.models.group import Group
    from db.models.bracket import Bracket


class NominationEvent(Base):
    __tablename__ = "nomination_event"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    nomination_id: Mapped[int] = mapped_column(ForeignKey("nomination.id"))

    registration_finished: bool = Column(Boolean, nullable=False, default=False)
    tournament_started: bool = Column(Boolean, nullable=False, default=False)
    type: NominationEventType = Column(String, nullable=False, default=NominationEventType.olympyc)

    groups: Mapped[list["Group"]] = relationship(
        "Group",
        back_populates="nomination_event"
    )
    bracket: Mapped["Bracket"] = relationship(
        "Bracket",
        back_populates="nomination_event"
    )

    judges: Mapped[list["User"]] = relationship(
        "User",
        back_populates="judged_events",
        secondary="nomination_event_judge"
    )

    team_participants: Mapped[list["TeamParticipant"]] = relationship(
        "TeamParticipant",
        back_populates="nomination_events",
        secondary="team_participant_nomination_event",
    )

    __table_args__ = (UniqueConstraint('event_id', 'nomination_id', 'type', name='_event_id__nomination_id__type'),)

