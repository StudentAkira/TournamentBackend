
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

from db.database import Base


class NominationEventJudge(Base):
    __tablename__ = "nomination_event_judge"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    nomination_event_id: int = Column(Integer, ForeignKey("nomination_event.id"))
    judge_id: int = Column(Integer, ForeignKey("users.id"))

    __table_args__ = (UniqueConstraint('id', 'nomination_event_id', 'judge_id', name='_id_nomination_event_id_judge_id'),)
