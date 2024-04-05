from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from db.database import Base


if TYPE_CHECKING:
    from db.models.nomination_event import NominationEvent
    from db.models.team import Team
    from db.models.match import BracketMatch


class Bracket(Base):
    __tablename__ = "tournament_bracket"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    nomination_event_id: int = Column(Integer, ForeignKey("nomination_event.id"), nullable=False)
    nomination_event: Mapped["NominationEvent"] = relationship(
        "NominationEvent",
        back_populates="bracket",
        foreign_keys="[Bracket.nomination_event_id]"
    )

    teams: Mapped[list["Team"]] = relationship(
        "Team",
        back_populates="brackets",
        secondary="bracket_team"
    )

    matches: Mapped[list["BracketMatch"]] = relationship("Match", back_populates="bracket")
