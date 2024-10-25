# Imports.
# External imports.
from enum import Enum, auto


# Body parts.
class BodyPart(Enum):
    HEAD = 0
    CHEST = 1
    RIGHT_HAND = 2
    LEFT_HAND = 3
    LEGS = 4


# Items.
class Items(Enum):
    RED_POTION = auto()
    LITLE_RED_POTION = auto()
    GIANT_RED_POTION = auto()
    ANTIDOTE = auto()


# Months.
class Months(Enum):
    AURENAR = 0
    SYLVANNA = 1
    IGNARIS = 2
    TEMPORA = 3
    OUSKARA = 4
    VALORA = 5
    NERITH = 6
    REVERIS = 7


class PlayerStatus(Enum):
    WALK = 0
    SURF = 1


# Seasons.
class Season(Enum):
    SPRING = 0
    SUMMER = 1
    AUTUMN = 2
    WINTER = 3


class TimeOfDay(Enum):
    MORNING = 0
    AFTERNOON = 1
    EVENING = 2
    NIGHT = 3


class WeekDays(Enum):
    SOLMAR = 0
    FIRNAR = 1
    LUNATHAR = 2
    ERATH = 3
    NYDAR = 4
    THORNAR = 5
    ELTHAR = 6
    KARNATH = 7
