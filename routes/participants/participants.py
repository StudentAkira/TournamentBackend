from typing import Annotated

from fastapi import APIRouter, Body

participants = APIRouter(prefix="/participants", tags=["auth"])


@participants.post("/create")
async def create_participant(token: Annotated[str, Body()], ):