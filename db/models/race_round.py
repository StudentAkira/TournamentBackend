from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import relationship, Mapped

from db.database import Base


if TYPE_CHECKING:
    from db.models.nomination_event import NominationEvent
    from db.models.team import Team


class RaceRound(Base):
    __tablename__ = "race_round"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_id: int = Column(Integer, ForeignKey("team.id"), nullable=False)
    team: Mapped["Team"] = relationship("Team", back_populates="race_rounds")

    result = Column(Numeric(precision=10, scale=3))

    nomination_event_id: int = Column(Integer, ForeignKey("nomination_event.id"), nullable=False)
    nomination_event: Mapped["NominationEvent"] = relationship(
        "NominationEvent",
        back_populates="race_rounds",
        foreign_keys="[RaceRound.nomination_event_id]"
    )
