from pydantic import BaseModel


class SoftwareSchema(BaseModel):
    name: str
