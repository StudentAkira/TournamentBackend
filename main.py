from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.requests import Request

from db import database, models
from routes.auth.auth import auth

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


@app.get('/')
async def main():
    return {"message": "hello world"}


app.include_router(auth)
