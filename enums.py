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


class EntryType(Enum):
    ARENA = 0
    BARRACKS = 1
    BLACKSMITH = 2
    CASTLE = 3
    CATHEDRAL = 4
    CAVERN = 5
    CHAPEL = 6
    COTTAGE = 7
    DUNGEON = 8
    FORTRESS = 9
    GRANARY = 10
    HALL = 11
    HUT = 12
    INN = 13
    LIBRARY = 14
    MARKET = 15
    MONASTERY = 16
    OUTPOST = 17
    PALACE = 18
    PORT = 19
    SANCTUARY = 20
    SHRINE = 21
    STABLES = 22
    TAVERN = 23
    TEMPLE = 24
    TOWER = 25
    VILLA = 26
    WATCHTOWER = 27


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


class NpcTypes(Enum):
    # Población general
    CAPTAIN = 0
    DRAGON = 1
    FISHERMAN = 2
    GUARD = 3
    INNKEEPER = 4
    LORD = 5
    MAYOR = 6
    MERCHANT = 7
    MONK = 8
    TRAVELER = 9
    WORKER = 10
    ALCHEMIST = 11
    BARD = 12
    BLACKSMITH = 13
    PRIEST = 14
    SORCERER = 15
    HUNTER = 16
    WITCH = 17
    FARMER = 18
    CARPENTER = 19
    SAILOR = 20
    SCHOLAR = 21
    THIEF = 22
    HEALER = 23
    EXPLORER = 24
    JESTER = 25
    COOK = 26
    ASSASSIN = 27
    MINER = 28
    HERMIT = 29
    KNIGHT = 30
    SHEPHERD = 31
    MERCENARY = 32
    ARTISAN = 33
    APPRENTICE = 34
    BEGGAR = 35
    DANCER = 36
    DIPLOMAT = 37
    SHAMAN = 38
    SMUGGLER = 39
    TAVERN_KEEPER = 40
    VETERAN = 41
    MAGE = 42
    CARAVAN_LEADER = 43
    LIBRARIAN = 44
    RANGER = 45
    CARTOGRAPHER = 46
    TAILOR = 47
    ORACLE = 48
    ENGINEER = 49
    SPY = 50

    # Nobleza y realeza
    BARON = 51
    BARONESS = 52
    VISCOUNT = 53
    VISCOUNTESS = 54
    COUNT = 55
    COUNTESS = 56
    MARQUIS = 57
    MARQUISE = 58
    DUKE = 59
    DUCHESS = 60
    GRAND_DUKE = 61
    GRAND_DUCHESS = 62
    PRINCE = 63
    PRINCESS = 64
    CROWN_PRINCE = 65
    CROWN_PRINCESS = 66
    KING = 67
    QUEEN = 68
    EMPEROR = 69
    EMPRESS = 70

    # Corte real
    ROYAL_ADVISOR = 71
    CHAMBERLAIN = 72
    COURT_MAGICIAN = 73
    COURT_JESTER = 74
    HANDMAIDEN = 75
    LADY_IN_WAITING = 76
    ROYAL_GUARD = 77
    ROYAL_HERALD = 78

    # Others.
    WHISPERS = 471993


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
