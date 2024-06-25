from pydantic import BaseModel


class AnnotationCreateSchema(BaseModel):
    text: str

    class Config:
        from_attributes = True
