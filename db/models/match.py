from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from db.database import Base


if TYPE_CHECKING:
    from db.models.group import Group
    from db.models.bracket import Bracket
    from db.models.team import Team


class Match(Base):
    __tablename__ = "match"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team1_id: int = Column(Integer, ForeignKey("team.id"), nullable=True)
    team1: Mapped["Team"] = relationship("Team", foreign_keys="[Match.team1_id]")

    team2_id: int = Column(Integer, ForeignKey("team.id"), nullable=True)
    team2: Mapped["Team"] = relationship("Team", foreign_keys="[Match.team2_id]")

    winner_id: int = Column(Integer, ForeignKey("team.id"))
    winner: Mapped["Team"] = relationship("Team", foreign_keys="[Match.winner_id]")

    group_id: int = Column(Integer, ForeignKey("tournament_group.id"), nullable=True)
    group: Mapped["Group"] = relationship("Group", back_populates="matches")

    match_queue_number: int = Column(Integer)

    bracket_id: int = Column(Integer, ForeignKey("tournament_bracket.id"), nullable=True)
    bracket: Mapped["Bracket"] = relationship("Bracket", back_populates="matches")
