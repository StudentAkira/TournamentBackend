from pydantic import BaseModel


class AnnotationDeleteSchema(BaseModel):
    id: int

    class Config:
        from_attributes = True
