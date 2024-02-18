from fastapi import FastAPI

from db import database, models

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


@app.get('/')
async def main():
    return {"message": "hello world"}
