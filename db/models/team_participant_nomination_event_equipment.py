from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from db.database import Base


class TeamParticipantNominationEventEquipment(Base):
    __tablename__ = "team_participants_nomination_event_equipment"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    team_participant_nomination_event_id: Mapped[int] =\
        mapped_column(ForeignKey("team_participant_nomination_event.id"))
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"))

    __table_args__ = (UniqueConstraint(
        'equipment_id',
        'team_participant_nomination_event_id',
        name='_team_participant_nomination_event_id_equipment_id'
    ),)
