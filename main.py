from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from config import get_settings
from db import database

from routes.auth.auth import auth
from routes.event.events import events
from routes.match.match import match
from routes.nomination_event.nomination_event import nomination_event
from routes.nomination.nomination import nominations
from routes.nomination_event_judge.nomination_event_judge import nomination_event_judge
from routes.participant.participants import participants
from routes.race_round.race_round import race_rounds
from routes.team.teams import teams
from routes.team_nomination_event.team_nomination_event import team_nomination_event
from routes.team_participant.team_participant import team_participant
from routes.team_participant_nomination_event.team_participant_nomination_event import team_participant_nomination_event
from routes.tournaments.tournaments import tournaments
from routes.user.users import users


settings = get_settings()


app = FastAPI()

from db.models.nominatuin_event_judge import NominationEventJudge
from db.models.group import Group
from db.models.bracket import Bracket
from db.models.group_team import GroupTeam
from db.models.bracket_team import BracketTeam
from db.models.match import Match
from db.models.race_round import RaceRound
from db.models.software import Software
from db.models.equipment import Equipment
from db.models.team_participant_nomination_event_software import TeamParticipantNominationEventSoftware
from db.models.team_participant_nomination_event_equipment import TeamParticipantNominationEventEquipment


database.Base.metadata.create_all(bind=database.engine)

origins = ['http://localhost:3000', 'http://127.0.0.1:3000',
           'https://localhost:3000', 'https://127.0.0.1:3000',
            'http://localhost:3001', 'http://127.0.0.1:3001',
           'http://127.0.0.1:9000', f"http://{settings.frontend_domain}",
            f"https://{settings.frontend_domain}", f"http://"
        ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": {"error": details[0]['msg']}}),
    )

@app.get('/')
async def main():
    return {"message": "hello world test"}


app.include_router(auth)
app.include_router(events)
app.include_router(nominations)
app.include_router(participants)
app.include_router(teams)
app.include_router(team_nomination_event)
app.include_router(team_participant)
app.include_router(team_participant_nomination_event)
app.include_router(users)
app.include_router(nomination_event_judge)
app.include_router(tournaments)
app.include_router(nomination_event)
app.include_router(match)
app.include_router(race_rounds)
