from pydantic import BaseModel


class EventGetNameSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
