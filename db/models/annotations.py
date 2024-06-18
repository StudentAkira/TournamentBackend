from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from db.database import Base


if TYPE_CHECKING:
    from db.models.user import User


class Annotation(Base):
    __tablename__ = "annotation"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    text = Column(String, unique=True)

    owner_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="annotations")
