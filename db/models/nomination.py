from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from db.database import Base

if TYPE_CHECKING:
    from db.models.event import Event


class Nomination(Base):
    __tablename__ = "nomination"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, unique=True)

    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="nominations",
        secondary="nomination_event"
    )
