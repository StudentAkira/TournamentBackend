from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Column, Integer, String
from phonenumbers import PhoneNumber
from sqlalchemy.orm import Mapped, relationship

from db.database import Base


if TYPE_CHECKING:
    from db.models.token import Token
    from db.models.event import Event
    from db.models.team import Team
    from db.models.participant import Participant
    from db.models.nomination_event import NominationEvent
    from db.models.match import Match
    from db.models.nomination import Nomination


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    email: EmailStr = Column(String, unique=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    first_name: str = Column(String, nullable=False)
    second_name: str = Column(String, nullable=False)
    third_name: str = Column(String, nullable=False)
    phone: str = Column(String, nullable=False)
    educational_institution: str | None = Column(String, nullable=True)
    role: str = Column(String, nullable=False)

    condemned_matches: Mapped[list["Match"]] = relationship("Match", back_populates="last_result_creator")
    tokens: Mapped[list["Token"]] = relationship("Token", back_populates="owner")
    events: Mapped[list["Event"]] = relationship("Event", back_populates="owner")
    nominations: Mapped[list["Nomination"]] = relationship("Nomination", back_populates="owner")
    created_teams: Mapped[list["Team"]] = relationship("Team", back_populates="creator")
    participants: Mapped[list["Participant"]] = relationship("Participant", back_populates="creator")
    judged_events: Mapped[list["NominationEvent"]] = relationship(
        "NominationEvent",
        back_populates="judges",
        secondary="nomination_event_judge"
    )
