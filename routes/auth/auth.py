from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.schemas import UserCreate
from dependencies import get_db

auth = APIRouter(prefix="/auth")


@auth.post("/login")
async def login():
    pass


@auth.post("logout")
async def logout():
    pass


@auth.post("/sign_in")
async def sign_in(user: UserCreate, db: Session = Depends(get_db)):
    pass
