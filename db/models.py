from phonenumbers import PhoneNumber
from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, Date
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .database import Base


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


class Token(Base):
    __tablename__ = "tokens"

    token: str = Column(String, unique=True, index=True, primary_key=True, nullable=False)
    owner_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="tokens")


class Participant(Base):
    __tablename__ = "participant"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    participant_email: EmailStr = Column(String, unique=True, nullable=False)
    first_name: str = Column(String, nullable=False)
    second_name: str = Column(String, nullable=False)
    third_name: str = Column(String, nullable=False)
    region: str = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    educational_institution: str = Column(String, nullable=False)
    additional_educational_institution: str = Column(String, nullable=False)

    teams: Mapped[list["Team"]] = relationship(
        back_populates="participants",
        secondary="team_participant"
    )


class NominationEvent(Base):
    __tablename__ = "nomination_event"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    nomination_id: Mapped[int] = mapped_column(ForeignKey("nomination.id"))

    __table_args__ = (UniqueConstraint('event_id', 'nomination_id', name='_event_id__nomination_id'),)

    teams: Mapped[list["Team"]] = relationship(
        back_populates="nomination_events",
        secondary="team_nomination_event"
    )


class Nomination(Base):
    __tablename__ = "nomination"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    events: Mapped[list["Event"]] = relationship(
        back_populates="nominations",
        secondary="nomination_event"
    )


class Event(Base):
    __tablename__ = "event"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, unique=True)

    owner_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner: Mapped[list["User"]] = relationship(back_populates="events")
    nominations: Mapped[list["Nomination"]] = relationship(
        back_populates="events",
        secondary="nomination_event"
    )


class Team(Base):
    __tablename__ = "team"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True, nullable=False)

    creator_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator: Mapped["User"] = relationship(back_populates="created_teams")

    nomination_events: Mapped[list["NominationEvent"]] = relationship(
        back_populates="teams",
        secondary="team_nomination_event"
    )
    participants: Mapped[list["Participant"]] = relationship(
        back_populates="teams",
        secondary="team_participant"
    )


class TeamNominationEvent(Base):
    __tablename__ = "team_nomination_event"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    nomination_event_id: Mapped[int] = mapped_column(ForeignKey("nomination_event.id"))

    softwares: Mapped[list["Software"]] = relationship(
        back_populates="team_nomination_events",
        secondary="software_team_nomination_event"
    )

    equipments: Mapped[list["Equipment"]] = relationship(
        back_populates="team_nomination_events",
        secondary="equipment_team_nomination_event"
    )


class Equipment(Base):
    __tablename__ = "equipment"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, unique=True)

    team_nomination_events: Mapped[list["TeamNominationEvent"]] = relationship(
        back_populates="equipments",
        secondary="equipment_team_nomination_event"
    )


class Software(Base):
    __tablename__ = "software"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, unique=True)

    team_nomination_events: Mapped[list["TeamNominationEvent"]] = relationship(
        back_populates="softwares",
        secondary="software_team_nomination_event"
    )


class SoftwareTeamNominationEvent(Base):
    __tablename__ = "software_team_nomination_event"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    software_id: Mapped[int] = Column(Integer, ForeignKey("software.id"))
    team_nomination_event_id: Mapped[int] = Column(Integer, ForeignKey("team_nomination_event.id"))


class EquipmentTeamNominationEvent(Base):
    __tablename__ = "equipment_team_nomination_event"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    equipment_id: Mapped[int] = Column(Integer, ForeignKey("equipment.id"))
    team_nomination_event_id: Mapped[int] = Column(Integer, ForeignKey("team_nomination_event.id"))


class TeamParticipant(Base):
    __tablename__ = "team_participant"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    participant_id: Mapped[int] = mapped_column(ForeignKey("participant.id"))

    # __table_args__ = (UniqueConstraint('team_id', 'participant_id', name='_team_id__nomination_event_id'),)





# class Equipment(Base):
#     __tablename__ = "equipment"
#
#     id: int = Column(Integer, primary_key=True, autoincrement=True)
#     name: str = Column(String, unique=True)
#
#     team_nomination_events: Mapped[list["TeamNominationEvent"]] = relationship(
#         back_populates="equipments",
#         secondary="equipment_team_nomination_event"
#     )
#



# class EquipmentTeamNominationEvent(Base):
#     __tablename__ = "equipment_team_nomination_event"
#
#     id: int = Column(Integer, primary_key=True, autoincrement=True)
#
#     equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"))
#     team_nomination_event_id: Mapped[int] = mapped_column("team_nomination_event.id")
#
