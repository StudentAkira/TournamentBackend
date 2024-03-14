from db.database import *
from db.models.component import Component
from db.models.device import Device
from db.models.user import User


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
