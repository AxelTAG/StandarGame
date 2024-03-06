# Imports.
# External imports
# Local imports.
from inventory import Inventory


# Player class.
class Player:
    def __init__(self, name: str = "", hp: int = 25, hpmax: int = 25, lvl: int = 1, exp: int = 0, expmax: int = 10,
                 attack: int = 2, defense: int = 1, evasion: int = 0, precision: int = 60, b_hpmax: int = 25,
                 b_attack: int = 2, b_defense: int = 1, b_evasion: int = 0, b_precision: int = 0.6, strength: int = 0,
                 agility: int = 0, vitality: int = 0, resistance: int = 0, dexterity: int = 0, x: int = 0, y: int = 0,
                 x_cp: int = 0, y_cp: int = int, st_points: int = 0, sk_points: int = 0, slot1: str = "Red Potion",
                 slot2: str = "Litle Red Potion", equip=None, inventory: Inventory = Inventory(), status: int = 0,
                 outside: bool = False):

        if len(name) > 12:
            self.name = name
        else:
            self.name = name[:12]
        self.hp = hp  # Hit points or life.
        self.hpmax = hpmax  # Max hit points or max life.
        self.lvl = lvl  # Level of player.
        self.exp = exp  # Actual experience points.
        self.expmax = expmax  # Max experience points for level up.
        self.attack = attack  # Current attack of player (base stats + equipment + others).
        self.defense = defense
        self.evasion = evasion
        self.precision = precision
        self.b_hpmax = b_hpmax
        self.b_attack = b_attack
        self.b_defense = b_defense
        self.b_evasion = b_evasion
        self.b_precision = b_precision
        self.strength = strength
        self.agility = agility
        self.vitality = vitality
        self.resistance = resistance
        self.dexterity = dexterity
        self.x = x
        self.y = y
        self.x_cp = x_cp
        self.y_cp = y_cp
        self.st_points = st_points
        self.sk_points = sk_points
        self.slot1 = slot1
        self.slot2 = slot2
        self.equip = equip

        if equip is None:
            self.equip = {"head": "None", "chest": "None", "right_hand": "None", "left_hand": "None", "legs": "None"}
        else:
            # Asegurarse de que equip sea un diccionario con las claves correctas
            valid_keys = {"head", "chest", "right_hand", "left_hand", "legs"}
            self.equip = {key: equip.get(key, "None") for key in valid_keys}

        self.inventory = inventory
        self.status = status  # 0: walk, 1: surf.
        self.events = {"message": False}
        self.outside = outside
