from db.database import *
from db import models, crud, schemas
from db.schemas.token import TokenDecodedSchema

db = SessionLocal()


td = TokenDecodedSchema(**{"user_id": 1, "role": "admin", "exp": 1})
