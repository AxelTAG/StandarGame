# Imports.
# External imports
# Local imports.
from inventory import Inventory


# Player class.
class Player:
    def __init__(self, name: str = "", hp: int = 25, hpmax: int = 25, lvl: int = 1, exp: int = 0, expmax: int = 10,
                 attack: int = 2, defense: int = 1, evasion: int = 0, precision: int = 60, strength: int = 0,
                 agility: int = 0, vitality: int = 0, resistance: int = 0, dexterity: int = 0, x: int = 0, y: int = 0,
                 x_cp: int = 0, y_cp: int = int, st_points: int = 0, sk_points: int = 0, slot1: str = "Red Potion",
                 slot2: str = "Litle Red Potion", equip=None, inventory: Inventory = Inventory(), walk: bool = True,
                 boat: bool = False):

        self.name = name
        self.hp = hp
        self.hpmax = hpmax
        self.lvl = lvl
        self.exp = exp
        self.expmax = expmax
        self.attack = attack
        self.defense = defense
        self.evasion = evasion
        self. precision = precision
        self.strength = strength
        self. agility = agility
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

        self.inventory = inventory
        self.walk = True
        self.boat = False
