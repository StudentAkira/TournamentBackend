from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

from db.database import Base

if TYPE_CHECKING:
    from db.models.user import User


class Token(Base):
    __tablename__ = "tokens"

    token: str = Column(String, unique=True, index=True, primary_key=True, nullable=False)
    owner_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="tokens")
