from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    judge = "judge"
    specialist = "specialist"