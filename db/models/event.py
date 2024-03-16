from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from db.database import Base

if TYPE_CHECKING:
    from db.models.user import User
    from db.models.nomination import Nomination


class Event(Base):
    __tablename__ = "event"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, unique=True)

    owner_id: int = Column(Integer, ForeignKey("user.id"), nullable=False)
    date: Date = Column(Date, nullable=False, default="2003-05-19")

    owner: Mapped[list["User"]] = relationship("User", back_populates="events")
    nominations: Mapped[list["Nomination"]] = relationship(
        "Nomination",
        back_populates="events",
        secondary="nomination_event",
    )
