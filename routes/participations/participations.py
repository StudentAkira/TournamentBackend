from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session

from db.schemas import Participant, Event, BaseNomination, Team, EventCreate
from dependencies import get_db
from routes.participations.participations_service import ParticipationsService

participations = APIRouter(prefix="/participations", tags=["participations"])


@participations.get("/events")
async def get_my_events(
        offset: Annotated[int, Query(gt=0)],
        limit: Annotated[int, Query(lt=50)],
        db: Session = Depends(get_db)
) -> list[Event]:
    service = ParticipationsService(db)
    return service.get_my_events(offset, limit)


@participations.get("/nominations")
async def get_nominations(
        offset: Annotated[int, Query(gt=0)],
        limit: Annotated[int, Query(lt=50)],
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


@participations.post("/create_nomination")
async def create_nominations(
        token: str,
        nominations: list[BaseNomination],
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.create_nominations(token, nominations)


@participations.post("/specify_nominations_for_event")
async def specify_nominations_for_event(
        token: str,
        event: Event,
        nominations: list[BaseNomination],
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.specify_nominations_for_event(token, event, nominations)


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
