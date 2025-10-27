# Imports.
# External imports.
from enum import Enum, auto


class Actions(Enum):
    ESCAPE = 0
    HIT_ATTACK = 1
    SKILL = 2
    USE_ITEM = 3
    WAIT = 4


class BodyPart(Enum):
    HEAD = 0
    CHEST = 1
    RIGHT_HAND = 2
    LEFT_HAND = 3
    LEGS = 4
    WAIST = 5


class EquipCondition(Enum):
    NECESSARY = 0
    NOT_NECESSARY = 1


class SkillElements(Enum):
    NEUTRAL = 0
    FIRE = 1
    EARTH = 2
    WATER = 3
    WIND = 4
    LIGHT = 5
    DARK = 6
    VOID = 7
    TIME = 8


class SkillType(Enum):
    ATTACK = 0
    DEFENSE = 1
    SUPPORT = 2


class EntryType(Enum):
    ARENA = 0
    BARRACKS = 1
    BLACKSMITH = 2
    CASTLE = 3
    CATHEDRAL = 4
    CAVE = 5
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
    SHIP = 28
    ROOM = 29
    HOUSE = 30
    POTION_SHOP = 31


class FirstMessages(Enum):
    MSG1 = "Nothing done yet."
    MSG2 = "Waiting for commands."


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
    # Población general.
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

    # Nobleza y realeza.
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

    # Corte real.
    ROYAL_ADVISOR = 71
    CHAMBERLAIN = 72
    COURT_MAGICIAN = 73
    COURT_JESTER = 74
    HANDMAIDEN = 75
    LADY_IN_WAITING = 76
    ROYAL_GUARD = 77
    ROYAL_HERALD = 78

    # Others.
    MONSTER = 79
    MAYORS_DAUGHTER = 80
    VILLAGER = 81
    ASTRONOMER = 82
    CARAVANNER = 83
    ANIMAL = 84
    ELDER = 85
    WHISPERS = 471993


class ObjectiveType(Enum):
    # Implemented.
    COLLECT = auto()
    KILL = auto()
    TALK = auto()
    DELIVER = auto()

    # Not implemented.
    ESCORT = auto()
    EXPLORE = auto()
    CRAFT = auto()
    PUZZLE = auto()
    TIMED = auto()
    DEFENSE = auto()
    INVESTIGATE = auto()
    DECISION = auto()


class PlayerStatus(Enum):
    WALK = 0
    SURF = 1
    FLY = 2


class QuestStatus(Enum):
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    REWARDED = auto()


class RequirementType(Enum):
    LVL = 0
    EQUIP = 1
    ITEM = 2
    STATS = 3
    VITAL_ENERGY = 4
    ALL_PAST = 9


class StatusType(Enum):
    POISON = auto()
    FREEZE = auto()
    BURN = auto()
    STUN = auto()
    BLEED = auto()
    PARALYSIS = auto()


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
