from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.team_nomination_event import AppendTeamParticipantNominationEventSchema, \
    DeleteTeamParticipantNominationEventSchema, UpdateTeamParticipantNominationEventSchema
from dependencies import get_db, authorized_only
from routes.team_participant_nomination_event.team_participant_nomination_event_service import \
    TeamParticipantNominationEventService

team_participant_nomination_event = APIRouter(
    prefix="/api/team_participant_nomination_event",
    tags=["team_participant_nomination_event"]
)


@team_participant_nomination_event.post("/team_participant")
async def append_team_participant_nomination_event(
        response: Response,
        team_participant_nomination_event_data: AppendTeamParticipantNominationEventSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamParticipantNominationEventService(db)
    return service.append_team_participant_nomination_event(
        response,
        token,
        team_participant_nomination_event_data
    )


@team_participant_nomination_event.put("/team_participant")
async def update_team_participant_nomination_event(
        response: Response,
        team_participant_nomination_event_data: UpdateTeamParticipantNominationEventSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamParticipantNominationEventService(db)
    return service.update_team_participant_nomination_event(
        response,
        token,
        team_participant_nomination_event_data
    )


@team_participant_nomination_event.delete("/team_participant")
async def delete_team_participant_nomination_event(
        response: Response,
        team_participant_nomination_event_data: DeleteTeamParticipantNominationEventSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamParticipantNominationEventService(db)
    return service.delete_team_participant_nomination_event(
        response,
        token,
        team_participant_nomination_event_data
    )
