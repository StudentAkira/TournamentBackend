from pydantic import BaseModel


class AnnotationUpdateSchema(BaseModel):
    id: int
    new_text: str

    class Config:
        from_attributes = True
