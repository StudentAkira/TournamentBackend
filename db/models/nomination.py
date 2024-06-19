from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from db.database import Base

if TYPE_CHECKING:
    from db.models.event import Event
    from db.models.user import User


class Nomination(Base):
    __tablename__ = "nomination"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, unique=False)

    owner_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="nominations")
    events: Mapped[list["Event"]] = relationship(
        "Event",
        secondary="nomination_event",
        back_populates="nominations",
    )

    __table_args__ = (UniqueConstraint('name', 'owner_id', name='_name_owner_id'),)
