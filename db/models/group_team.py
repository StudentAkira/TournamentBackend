from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class GroupTeam(Base):
    __tablename__ = "group_team"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))

    __table_args__ = (UniqueConstraint('team_id', 'group_id', name='_team_id__group_id'),)
