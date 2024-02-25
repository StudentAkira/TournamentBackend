from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas import Participant, Event, BaseNomination, Team, EventCreate, Equipment, Software
from dependencies import get_db, authorized_only
from routes.participations.participations_service import ParticipationsService

participations = APIRouter(prefix="/participations", tags=["participations"])


@participations.get("/event")
async def get_events(
        offset: Annotated[int, Query(gte=0, lt=50)],
        limit: Annotated[int, Query(lt=50, gt=0)],
        db: Session = Depends(get_db)
) -> list[Event]:
    service = ParticipationsService(db)
    return service.get_events(offset, limit)


@participations.get("/nominations")
async def get_nominations(
        offset: Annotated[int, Query(gte=0, lt=50)],
        limit: Annotated[int, Query(lt=50, gt=0)],
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.get_nominations(offset, limit)


@participations.post("/event")
async def create_event(
        response: Response,
        event: EventCreate,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.create_event(response, token, event)


@participations.post("/nominations")
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


@participations.post("/teams")
async def create_team(
        response: Response,
        team: Team,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.create_team(response, token, team)


@participations.get("/teams")
async def get_teams(
        response: Response,
        offset: Annotated[int, Query(gte=0, lt=50)],
        limit: Annotated[int, Query(lt=50, gt=0)],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)):
    service = ParticipationsService(db)
    return service.get_my_teams(response, token, offset, limit)


@participations.post("/participant")
async def create_participant(
        response: Response,
        participant: Participant,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.create_participant(response, token, participant)


@participations.post("/append_teams_for_participant")
async def append_teams_for_participant(
        response: Response,
        teams: list[Team],
        participant: Participant,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.append_teams_for_participant(response, token, teams, participant)


@participations.post("/append_participants_for_team")
async def append_participants_for_team(
        response: Response,
        team: Team,
        participants: list[Participant],
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = ParticipationsService(db)
    return service.append_participants_for_team(response, token, team, participants)


@participations.post("/software")
async def create_software(response: Response, software: list[Software], token: str = Depends(authorized_only), db: Session = Depends(get_db)):
    service = ParticipationsService(db)
    return service.create_software(response, token, software)


@participations.post("/equipment")
async def create_equipment(response: Response, equipment: list[Equipment], token: str = Depends(authorized_only), db: Session = Depends(get_db)):
    service = ParticipationsService(db)
    return service.create_equipment(response, token, equipment)
