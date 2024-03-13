import time
from random import randint

from sqlalchemy import and_

from db.crud.nomination_event import get_nomination_event_db
from db.database import *
from db import models
from db.schemas.nomination_event import NominationEventSchema
from db.schemas.team import TeamParticipantsSchema


db = SessionLocal()


def counting_sort(arr):
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    sorted_arr = []
    for i in range(len(count)):
        sorted_arr.extend([i] * count[i])
    return sorted_arr


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


# Example usage:
arr = [randint(1, 1000000) for x in range(10000000, 0, -1)]
start = time.time()
counting_sort(arr)
print(time.time() - start)

start = time.time()
quicksort(arr)
print(time.time() - start)

#
# events_db = db.query(models.Event).all()
# nomination_event_full_info_list = []
# for event_db in events_db:
#     for nomination_db in event_db.nominations:
#         nomination_event_db = db.query(models.NominationEvent).\
#             filter(and_(models.NominationEvent.nomination_id == nomination_db.id, models.NominationEvent.event_id == event_db.id)).first()
#
#         team_ids = set(team_participant.team_id for team_participant in nomination_event_db.team_participants)
#         participant_ids = [team_participant.participant_id for team_participant in nomination_event_db.team_participants]
#
#         team_id_data = db.query(models.Team.id, models.Team).filter(models.Team.id.in_(team_ids)).all()
#         participant_id_data = db.query(models.Participant.id, models.Participant).filter(
#             models.Participant.id.in_(participant_ids)).all()
#
#         team_id_names_dict = {key: value for key, value in team_id_data}
#         participant_id_email_dict = {key: value for key, value in participant_id_data}
#
#         teams = []
#
#         for team_id in team_ids:
#             team = team_id_names_dict[team_id]
#             teams.append(team)
#
#         print(event_db.name)
#         print("\t", nomination_db.name)
#
#         nomination_event_full_info = NominationEventSchema(
#             event_name=event_db.name,
#             nomination_name=nomination_db.name,
#             teams=[
#                 TeamParticipantsSchema.from_orm(
#                     team
#                 ) for team in teams
#             ]
#         )
#
#     nomination_event_full_info_list.append(nomination_event_full_info)

