from phonenumbers import PhoneNumber
from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Date, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .database import Base
from .schemas.nomination_event import NominationEventType


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    email: EmailStr = Column(String, unique=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    first_name: str = Column(String, nullable=False)
    second_name: str = Column(String, nullable=False)
    third_name: str = Column(String, nullable=False)
    phone: PhoneNumber = Column(String, nullable=False)
    educational_institution: str | None = Column(String, nullable=True)
    role: str = Column(String, nullable=False)

    tokens: Mapped[list["Token"]] = relationship(back_populates="owner")
    events: Mapped[list["Event"]] = relationship(back_populates="owner")
    created_teams: Mapped[list["Team"]] = relationship(back_populates="creator")
    participants: Mapped[list["Participant"]] = relationship(back_populates="creator")


class Token(Base):
    __tablename__ = "tokens"

    token: str = Column(String, unique=True, index=True, primary_key=True, nullable=False)
    owner_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="tokens")


class Participant(Base):
    __tablename__ = "participant"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    email: EmailStr = Column(String, unique=True, nullable=False)
    first_name: str = Column(String, nullable=False)
    second_name: str = Column(String, nullable=False)
    third_name: str = Column(String, nullable=False)
    region: str = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    educational_institution: str = Column(String, nullable=False)
    additional_educational_institution: str = Column(String, nullable=False)
    supervisor_first_name: str = Column(String, nullable=False)
    supervisor_second_name: str = Column(String, nullable=False)
    supervisor_third_name: str = Column(String, nullable=False)

    creator_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator: Mapped["User"] = relationship("User", back_populates="participants")

    teams: Mapped[list["Team"]] = relationship(
        back_populates="participants",
        secondary="team_participant"
    )


class NominationEvent(Base):
    __tablename__ = "nomination_event"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    nomination_id: Mapped[int] = mapped_column(ForeignKey("nomination.id"))

    registration_finished: bool = Column(Boolean, nullable=False, default=False)
    type: NominationEventType = Column(String, nullable=False, default=NominationEventType.olympyc)

    team_participants: Mapped[list["TeamParticipant"]] = relationship(
        back_populates="nomination_events",
        secondary="team_participant_nomination_event"
    )

    __table_args__ = (UniqueConstraint('event_id', 'nomination_id', name='_event_id__nomination_id'),)


class Nomination(Base):
    __tablename__ = "nomination"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, unique=True)

    events: Mapped[list["Event"]] = relationship(
        back_populates="nominations",
        secondary="nomination_event"
    )


class Event(Base):
    __tablename__ = "event"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, unique=True)

    owner_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    date: Date = Column(Date, nullable=False, default="2003-05-19")

    owner: Mapped[list["User"]] = relationship(back_populates="events")
    nominations: Mapped[list["Nomination"]] = relationship(
        back_populates="events",
        secondary="nomination_event",
    )


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


class TeamParticipant(Base):
    __tablename__ = "team_participant"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    participant_id: Mapped[int] = mapped_column(ForeignKey("participant.id"))

    nomination_events: Mapped[list["NominationEvent"]] = relationship(
        back_populates="team_participants",
        secondary="team_participant_nomination_event"
    )

    __table_args__ = (UniqueConstraint('team_id', 'participant_id', name='_team_id__particiapant_id'),)


class TeamParticipantNominationEvent(Base):
    __tablename__ = "team_participant_nomination_event"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_participant_id: Mapped["int"] = mapped_column(ForeignKey("team_participant.id"))
    nomination_event_id: Mapped["int"] = mapped_column(ForeignKey("nomination_event.id"))

    equipment = Column(String)
    software = Column(String)


class Match(Base):
    __tablename__ = "match"

    id: int = Column(Integer, primary_key=True, autoincrement=True)


class Group(Base):
    __tablename__ = "group"

    id: int = Column(Integer, primary_key=True, autoincrement=True)


class Grid(Base):
    __tablename__ = "grid"

    id: int = Column(Integer, primary_key=True, autoincrement=True)