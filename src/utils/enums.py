from enum import Enum, IntEnum


class Priorities(IntEnum):
    TOP = 0
    MIDDLE = 1
    STANDARD = 2


class Statuses(Enum):
    CREATED = "К выполнению"
    IN_WORK = "В работе"
    ON_MODERATION = "На проверке"
    CANCELED = "Отменена"
    DONE = "Выполнена"
