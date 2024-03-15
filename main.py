from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import database

from routes.auth.auth import auth
from routes.event.events import events
from routes.nomination_event.nomination_event import nomination_event
from routes.nomination.nominations import nominations
from routes.participant.participants import participants
from routes.team.teams import teams
from routes.team_participant.team_participant import team_participant
from routes.tournament_registration.tournament_registration import tournament_registration
from routes.tournaments.tournaments import tournaments
from routes.user.users import users


app = FastAPI()


database.Base.metadata.create_all(bind=database.engine)

origins = ['http://localhost:3000', 'http://127.0.0.1:3000',
           'https://localhost:3000', 'https://127.0.0.1:3000',
            'http://localhost:3001', 'http://127.0.0.1:3001',
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def main():
    return {"message": "hello world"}


app.include_router(auth)
app.include_router(events)
app.include_router(nominations)
app.include_router(participants)
app.include_router(teams)
app.include_router(team_participant)
app.include_router(tournament_registration)
app.include_router(users)
app.include_router(tournaments)
app.include_router(nomination_event)

