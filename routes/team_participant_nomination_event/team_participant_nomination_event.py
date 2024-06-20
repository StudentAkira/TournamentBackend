from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from db.schemas.team_nomination_event.delete_team_participant_nomination_event import \
    DeleteTeamParticipantNominationEventSchema
from db.schemas.team_nomination_event.update_team_participant_nomination_event import \
    UpdateTeamParticipantNominationEventSchema
from db.schemas.team_participant_nomination_event.append_teams_participants_nomination_event import \
    TeamParticipantNominationEventAppendSchema
from dependencies.dependencies import get_db, authorized_only
from routes.team_participant_nomination_event.team_participant_nomination_event_service import \
    TeamParticipantNominationEventService
from urls import URLs

team_participant_nomination_event = APIRouter(
    prefix=URLs.team_participant_nomination_event_prefix.value,
    tags=URLs.team_participant_nomination_event_tags.value
)


@team_participant_nomination_event.post(URLs.team_participant.value)
async def append_team_participant_nomination_event(
        response: Response,
        team_participant_nomination_event_data: TeamParticipantNominationEventAppendSchema,
        token: str = Depends(authorized_only),
        db: Session = Depends(get_db)
):
    service = TeamParticipantNominationEventService(db)
    return service.append_team_participant_nomination_event(
        response,
        token,
        team_participant_nomination_event_data
    )


@team_participant_nomination_event.put(URLs.team_participant.value, deprecated=True)
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


@team_participant_nomination_event.delete("/team_participant", deprecated=True)
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
