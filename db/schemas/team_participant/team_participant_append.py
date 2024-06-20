from pydantic import BaseModel

from db.schemas.equipment.equipment import EquipmentSchema
from db.schemas.software.software import SoftwareSchema


class TeamParticipantAppendSchema(BaseModel):
    participant_id: int
    softwares: list[SoftwareSchema]
    equipments: list[EquipmentSchema]
