from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    third_name = Column(String, nullable=False)

    phone = Column(String, nullable=False)
    educational_institution = Column(String, nullable=True)

    role = Column(String, nullable=False)
    tokens = relationship("Token", back_populates="owner")


class Token(Base):
    __tablename__ = "tokens"

    token = Column(String, unique=True, index=True, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tokens")


class Participant(Base):
    __tablename__ = "participant"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)

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


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)

    name = Column(String, unique=True, nullable=False)


participant_team = Table("participant_team", Base.metadata,
                         Column("participant_id", ForeignKey("participant.id"), primary_key=True, nullable=False),
                         Column("team_id", ForeignKey("team.id"), primary_key=True, nullable=False)
                         )


class Nomination(Base):
    __tablename__ = "nomination"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)

    name = Column(String, unique=True, nullable=False)


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)

    name = Column(String, unique=True, nullable=False)


event_nomination = Table("event_nomination", Base.metadata,
                         Column("id", Integer, primary_key=True, autoincrement=True,  unique=True, nullable=False),
                         Column("event_id", ForeignKey("event.id"), primary_key=True, nullable=False),
                         Column("nomination_id", ForeignKey("nomination.id"), primary_key=True, nullable=False)
                         )

team_event_nomination = Table("team_event_nomination", Base.metadata,
                              Column("team_id", ForeignKey("team.id"), primary_key=True, nullable=False),
                              Column("event_nomination_id", ForeignKey("event_nomination.id"), primary_key=True, nullable=False),
                              )


class Match(Base):
    __tablename__ = "match"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)

    team1_id = Column(Integer, nullable=True)
    team2_id = Column(Integer, nullable=True)
    winner_id = Column(Integer, nullable=True)

    event_nomination_id = Column(Integer, ForeignKey("event_nomination.id"), nullable=False)
    event_nomination = relationship("event_nomination", back_populates="event_nomination")


class MatchGrid(Base):
    __tablename__ = "match_grid"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)

    match_id = Column(Integer, ForeignKey("match.id"), nullable=False)
    status = Column(Integer, nullable=False)


class MatchGroup(Base):
    __tablename__ = "match_group"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)

    group_name = Column(String, nullable=False)
    match_id = Column(Integer, ForeignKey("match.id"), nullable=False)
