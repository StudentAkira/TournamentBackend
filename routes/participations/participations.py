from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, Cookie
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas import Participant, Event, BaseNomination, Team, EventCreate
from dependencies import get_db, authorized_only
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
        response: Response,
        event: EventCreate,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.create_event(response, token, event)


@participations.post("/create_nominations")
async def create_nominations(
        response: Response,
        nominations: list[BaseNomination],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.create_nominations(response, token, nominations)


@participations.post("/append_nominations_for_event")
async def append_nominations_for_event(
        response: Response,
        event: Event,
        nominations: list[BaseNomination],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.append_nominations_for_event(response, token, event, nominations)


@participations.post("/create_team")
async def create_team(
        response: Response,
        team: Team,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.create_team(response, token, team)


@participations.post("/create_participant")
async def create_participant(
        response: Response,
        participant: Participant,
        teams: list[Team] | None = None,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.create_participant(response, token, participant, teams)


@participations.post("/specify_teams_for_participant")
async def specify_nominations_for_event(
        response: Response,
        teams: list[Team],
        participant: Participant,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.specify_teams_for_participant(response, token, teams, participant)
