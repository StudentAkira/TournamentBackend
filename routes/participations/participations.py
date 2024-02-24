from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session

from db.schemas import Participant, Event, BaseNomination, Team, EventCreate
from dependencies import get_db
from routes.participations.participations_service import ParticipationsService

participations = APIRouter(prefix="/participations", tags=["participations"])


@participations.get("/events")
async def get_events(
        offset: Annotated[int, Query(gt=0, lt=50)],
        limit: Annotated[int, Query(lt=50, gt=0)],
        db: Session = Depends(get_db)
) -> list[Event]:
    service = ParticipationsService(db)
    return service.get_events(offset, limit)


@participations.get("/nominations")
async def get_nominations(
        offset: Annotated[int, Query(gt=0, lt=50)],
        limit: Annotated[int, Query(lt=50, gt=0)],
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.get_nominations(offset, limit)


@participations.post("/create_event")
async def create_event(
        token: Annotated[str, Body()],
        event: EventCreate,
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.create_event(token, event)


@participations.post("/create_nominations")
async def create_nominations(
        token: Annotated[str, Body()],
        nominations: list[BaseNomination],
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.create_nominations(token, nominations)


@participations.post("/append_nominations_for_event")
async def append_nominations_for_event(
        token: Annotated[str, Body()],
        event: Event,
        nominations: list[BaseNomination],
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.append_nominations_for_event(token, event, nominations)


@participations.post("/create_team")
async def create_team(
        token: str,
        team: Team,
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.create_team(token, team)


@participations.post("/create_participant")
async def create_participant(
        token: str,
        participant: Participant,
        teams: list[Team] | None = None,
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.create_participant(token, participant, teams)


@participations.post("/specify_teams_for_participant")
async def specify_nominations_for_event(
        token: str,
        teams: list[Team],
        participant: Participant,
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.specify_teams_for_participant(token, teams, participant)
