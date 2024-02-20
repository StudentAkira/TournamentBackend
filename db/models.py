from sqlalchemy import Column, Integer, String, ForeignKey
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


class Token(Base):
    __tablename__ = "tokens"
    token = Column(String, unique=True, index=True, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tokens")
