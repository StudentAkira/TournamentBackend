from pydantic import BaseModel


class EquipmentSchema(BaseModel):
    name: str
