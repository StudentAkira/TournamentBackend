from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class GroupTeam(Base):
    __tablename__ = "group_team"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    tournament_group_id: Mapped[int] = mapped_column(ForeignKey("tournament_group.id"))

    __table_args__ = (UniqueConstraint('team_id', 'tournament_group_id', name='_team_id__tournament_group_id'),)
