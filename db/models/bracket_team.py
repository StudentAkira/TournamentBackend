from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class BracketTeam(Base):
    __tablename__ = "bracket_team"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    bracket_id: Mapped[int] = mapped_column(ForeignKey("tournament_bracket.id"))

    __table_args__ = (UniqueConstraint('team_id', 'bracket_id', name='_team_id__bracket_id'),)
