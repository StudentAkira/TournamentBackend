from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import database, models
from routes.auth.auth import auth
from routes.equipment.equipment import equipment
from routes.events.events import events
from routes.nominations.nominations import nominations
from routes.participants.participants import participants
from routes.software.software import software
from routes.teams.teams import teams
from routes.tournament_registration.tournament_registration import tournament_registration
from routes.users.users import users


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

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
app.include_router(equipment)
app.include_router(events)
app.include_router(nominations)
app.include_router(participants)
app.include_router(software)
app.include_router(teams)
app.include_router(tournament_registration)
app.include_router(users)
