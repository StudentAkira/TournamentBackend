from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import database, models
from routes.auth.auth import auth
from routes.participations.participations import participations
from routes.users.users import users

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

origins = [
    "http://localhost:3000",
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
app.include_router(users)
app.include_router(participations)
