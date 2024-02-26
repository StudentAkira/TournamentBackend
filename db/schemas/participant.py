import datetime

from pydantic import BaseModel, EmailStr


class ParticipantSchema(BaseModel):
    email: EmailStr
    first_name: str
    second_name: str
    third_name: str
    region: str
    birth_date: datetime.date
    educational_institution: str
    additional_educational_institution: str
    supervisor_first_name: str
    supervisor_second_name: str
    supervisor_third_name: str

    class Config:
        from_attributes = True
