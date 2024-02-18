from fastapi import APIRouter


tournament = APIRouter(prefix="/tournament", tags=["tournament"])


@tournament.post("/create_tournament")
async def create_tournament(tournament_name: str):
    pass


@tournament.post("/set_tournament_participants")
async def set_tournament_participants(tournament_id: int, participants_usernames: list[str]):
    pass


@tournament.post("/set_match_results")
async def set_match_results(results: list[tuple[str, int]]):
    pass