from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    third_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    educational_institution = Column(String, nullable=True)
    role = Column(String, nullable=False)

    tokens = relationship("Token", back_populates="owner")
    events = relationship("Event", back_populates="owner")


class Token(Base):
    __tablename__ = "tokens"

    token = Column(String, unique=True, index=True, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tokens")


class Participant(Base):
    __tablename__ = "participant"

    id = Column(Integer, primary_key=True, autoincrement=True)

    participant_email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    third_name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    team_name = Column(Integer, nullable=False)
    competence_id = Column(Integer, nullable=False)
    birth_date = Column(DateTime, nullable=False)
    software = Column(String, nullable=True)
    imported_equipment = Column(String, nullable=True)
    educational_institution = Column(String, nullable=False)
    additional_educational_institution = Column(String, nullable=False)


# class Team(Base):
#     __tablename__ = "team"
#
#     id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
#
#     nomination_events: Mapped[list["NominationEvent"]] = relationship(
#         back_populates="teams",
#         secondary="TeamNominationEvent"
#
#     )


class NominationEvent(Base):
    __tablename__ = "nomination_event"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)

    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)
    nomination_id: Mapped[int] = mapped_column(ForeignKey("nomination.id"), primary_key=True)

    __table_args__ = (UniqueConstraint('event_id', 'nomination_id', name='_event_id__nomination_id'),
                      )

    # teams: Mapped[list["Team"]] = relationship(
    #     back_populates="nomination_events",
    #     secondary="TeamNominationEvent"
    # )


class Nomination(Base):
    __tablename__ = "nomination"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    events: Mapped[list["Event"]] = relationship(
        back_populates="nominations",
        secondary="nomination_event"
    )


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[int] = Column(String, unique=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner: Mapped[list["User"]] = relationship( back_populates="events")
    nominations: Mapped[list["Nomination"]] = relationship(
        back_populates="events",
        secondary="nomination_event"
    )


# class TeamNominationEvent(Base):
#     __tablename__ = "team_nomination_event"
#
#     id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
#
#     team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), primary_key=True)
#     nomination_event_id: Mapped[int] = mapped_column(ForeignKey("nomination_event.id"), primary_key=True)
#
#
#
#
#




# class Match(Base):
#     __tablename__ = "match"
#
#     id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
#
#     team1_id = Column(Integer, nullable=True)
#     team2_id = Column(Integer, nullable=True)
#     winner_id = Column(Integer, nullable=True)
#
#     event_nomination_id = Column(Integer, ForeignKey("event_nomination.id"), nullable=False)
#     event_nomination = relationship("event_nomination", back_populates="matches")
#
#
# class MatchGrid(Base):
#     __tablename__ = "match_grid"
#
#     id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
#
#     match_id = Column(Integer, ForeignKey("match.id"), nullable=False)
#     status = Column(Integer, nullable=False)
#
#
# class MatchGroup(Base):
#     __tablename__ = "match_group"
#
#     id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
#
#     group_name = Column(String, nullable=False)
#     match_id = Column(Integer, ForeignKey("match.id"), nullable=False)
