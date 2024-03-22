from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from db.database import Base


if TYPE_CHECKING:
    from db.models.user import User
    from db.models.participant import Participant
    from db.models.group import Group
    from db.models.bracket import Bracket
    from db.models.match import Match


class Team(Base):
    __tablename__ = "team"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True, nullable=True)

    creator_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator: Mapped["User"] = relationship("User", back_populates="created_teams")

    match_team1_id: int = Column(Integer, ForeignKey("match.id"), nullable=False)
    match_team1: Mapped[list["Match"]] = relationship("Match", back_populates="team1")

    match_team2_id: int = Column(Integer, ForeignKey("match.id"), nullable=False)
    match_team2: Mapped[list["Match"]] = relationship("Match", back_populates="team2")

    participants: Mapped[list["Participant"]] = relationship(
        "Participant",
        back_populates="teams",
        secondary="team_participant"
    )

    groups: Mapped[list["Group"]] = relationship(
        "Group",
        back_populates="teams",
        secondary="group_team"
    )

    brackets: Mapped[list["Bracket"]] = relationship(
        "Bracket",
        back_populates="teams",
        secondary="bracket_team"
    )
