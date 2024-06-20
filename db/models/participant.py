from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped

from db.database import Base


if TYPE_CHECKING:
    from db.models.user import User
    from db.models.team import Team


class Participant(Base):
    __tablename__ = "participant"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    email: EmailStr = Column(String, unique=True, nullable=False)
    first_name: str = Column(String, nullable=False)
    second_name: str = Column(String, nullable=False)
    third_name: str = Column(String, nullable=True)
    region: str = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    educational_institution: str = Column(String, nullable=False)
    additional_educational_institution: str = Column(String, nullable=True)
    supervisor_first_name: str = Column(String, nullable=False)
    supervisor_second_name: str = Column(String, nullable=False)
    supervisor_third_name: str = Column(String, nullable=False)

    creator_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator: Mapped["User"] = relationship("User", back_populates="participants")

    teams: Mapped[list["Team"]] = relationship(
        "Team",
        back_populates="participants",
        secondary="team_participant"
    )
