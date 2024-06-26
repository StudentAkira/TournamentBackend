from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.nomination_event.time_nomination_event import TimeNominationEventSchema
from db.schemas.race_round.race_round_create import RaceRoundCreateSchema
from db.schemas.race_round.race_round_update import RaceRoundUpdateSchema
from dependencies import get_db, authorized_only
from routes.race_round.race_round_service import RaceRoundService

race_rounds = APIRouter(prefix="/api/race_round", tags=["race_round"])


@race_rounds.get("/race_round")
async def get_race_rounds(
        response: Response,
        event_name: Annotated[str, Query()],
        nomination_name: Annotated[str, Query()],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = RaceRoundService(db)
    return service.get_race_rounds(response, token, event_name, nomination_name)


@race_rounds.post("/race_round")
async def create_race_round(
        response: Response,
        race_round: RaceRoundCreateSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = RaceRoundService(db)
    return service.set_race_rounds(response, token, race_round)


@race_rounds.put("/race_round")
async def update_race_round(
        response: Response,
        race_round: RaceRoundUpdateSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = RaceRoundService(db)
    return service.update_race_rounds(response, token, race_round)
