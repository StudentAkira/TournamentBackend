import time

from db.database import *
from db import models, crud, schemas
from db.schemas.token import TokenDecodedSchema

db = SessionLocal()


td = TokenDecodedSchema(**{"user_id": 1, "role": "admin", "exp": 1})


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[int(len(arr) / 2)]
    left = []
    middle = []
    right = []
    for x in arr:
        if x < pivot:
            left.append(x)
        elif x == pivot:
            middle.append(x)
        elif x > pivot:
            right.append(x)
    return quicksort(left) + middle + quicksort(right)


start = time.time()
quicksort([x for x in range(1000000,0,-1)])
print(time.time() - start)
