from fastapi import FastAPI
from db import database, models
from routes.auth.auth import auth
from routes.tournament.tournament import tournament

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


@app.get('/')
async def main():
    return {"message": "hello world"}


app.include_router(auth)
app.include_router(tournament)
