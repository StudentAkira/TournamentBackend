from pydantic import BaseModel

from db.schemas.user.user import UserSchema


class NominationEventJudgesSchema(BaseModel):
    judges: list[UserSchema]
