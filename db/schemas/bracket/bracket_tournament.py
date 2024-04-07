from pydantic import BaseModel

from db.schemas.match.bracket_match_schema import BracketMatchSchema


class BracketMatchesSchema(BaseModel):

    matches: list[BracketMatchSchema]

    class Config:
        from_attributes = True
