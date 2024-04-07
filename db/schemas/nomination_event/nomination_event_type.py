from enum import Enum


class NominationEventType(str, Enum):
    olympyc = "olympyc"
    time = "time"
    criteria = "criteria"