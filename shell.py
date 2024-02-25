from db.database import *
from db import models, crud, schemas

db = SessionLocal()

nominations = [
    schemas.BaseNomination(name="nomination1"),
    schemas.BaseNomination(name="nomination2")
]

event_create = schemas.EventCreate(name="event1", nominations=nominations)

admin = db.query(models.User).filter(models.User.id == 1).first()

team = models.Team(name="team1")
# event = db.query(models.Event).filter(models.Event.name == "event6").first()


# event = models.Event(owner_id=1, name="event1")

# event_create = schemas.EventCreate(name="event1", nominations=nominations)
#
# db_nominations = crud.create_nominations_db(db, nominations)
#
# nomination_event0 = models.NominationEvent(
#     event=event,
#     nomination=db_nominations[0]
# )
#
# nomination_event1 = models.NominationEvent(
#     event=event,
#     nomination=db_nominations[1]
# )
