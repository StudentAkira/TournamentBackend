from pydantic import BaseModel, Field

from db.schemas.nomination import NominationSchema


class EventSchema(BaseModel):
    name: str = Field(min_length=5)

    class Config:
        from_attributes = True


class EventCreateSchema(EventSchema):
    nominations: list[NominationSchema] | None
