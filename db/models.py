from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    third_name = Column(String, nullable=False)

    phone = Column(String, nullable=False)
    educational_institution = Column(String, nullable=True)

    role = Column(String, nullable=False)
    tokens = relationship("Token", back_populates="owner")
    participants = relationship("Participant", back_populates="creator")


class Token(Base):
    __tablename__ = "tokens"
    token = Column(String, unique=True, index=True, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tokens")


class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True)
    participant_email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    third_name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    team_name = Column(Integer, nullable=False)
    competence_id = Column(Integer, nullable=False)
    birth_date = Column(DateTime)
    software = Column(String)
    imported_equipment = Column(String)
    educational_institution = Column(String)
    additional_educational_institution = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator = relationship("User", back_populates="participants")


class Team(Base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
