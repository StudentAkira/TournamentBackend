from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.database import Base


if TYPE_CHECKING:
    from db.models.nomination_event import NominationEvent
    from db.models.team import Team
    from db.models.match import Match


class Group(Base):
    __tablename__ = "tournament_group"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    nomination_event_id: int = Column(Integer, ForeignKey("nomination_event.id"), nullable=False)
    nomination_event: Mapped["NominationEvent"] = relationship(
        "NominationEvent",
        back_populates="groups",
        foreign_keys="[Group.nomination_event_id]"
    )

    teams: Mapped[list["Team"]] = relationship(
        "Team",
        back_populates="groups",
        secondary="group_team"
    )

    matches: Mapped[list["Match"]] = relationship("Match", back_populates="group")
