from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from db.schemas import Participant
from dependencies import get_db
from routes.participations.participations_service import ParticipationsService

participations = APIRouter(prefix="/participations", tags=["auth"])


@participations.post("/create_team")
async def create_team():
    pass


@participations.post("/create_participant")
async def create_participant():
    pass


@participations.post("/create_event")
async def create_event():
    pass


@participations.post("create_nomination")
async def create_nomination():
    pass
