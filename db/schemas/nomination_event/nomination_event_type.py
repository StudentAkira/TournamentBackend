from enum import Enum


class NominationEventType(str, Enum):
    olympyc = "olympic"
    time = "time"
    criteria = "criteria"
