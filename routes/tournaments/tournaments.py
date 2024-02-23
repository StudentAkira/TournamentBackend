from fastapi import APIRouter


tournaments = APIRouter(prefix="/tournaments", tags=["tournaments"])


@tournaments.post("/start_group_tournament")
async def start_group_tournament():
    pass


@tournaments.post("/start_play_off_tournament")
async def start_play_off_tournament():
    pass
