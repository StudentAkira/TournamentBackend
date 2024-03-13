from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from db.database import Base


if TYPE_CHECKING:
    from db.models.user import User
    from db.models.participant import Participant


class Team(Base):
    __tablename__ = "team"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True, nullable=True)

    creator_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator: Mapped["User"] = relationship(back_populates="created_teams")

    participants: Mapped[list["Participant"]] = relationship(
        back_populates="teams",
        secondary="team_participant"
    )
