from pydantic import BaseModel


class AnnotationGetSchema(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True

