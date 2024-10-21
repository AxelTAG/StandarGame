# Imports.
# Local imports.
from inventory import Inventory

# External imports.
import numpy as np
from datetime import timedelta


# Player class.
class Player:
    def __init__(self,
                 name: str = "",
                 hp: int = 25,
                 hpmax: int = 25,
                 lvl: int = 1,
                 exp: int = 0,
                 expmax: int = 10,
                 attack: int = 2,
                 defense: int = 1,
                 evasion: int = 0,
                 precision: int = 60,
                 b_hpmax: int = 25,
                 b_attack: int = 2,
                 b_defense: int = 1,
                 b_evasion: int = 0,
                 b_precision: int = 0.6,
                 strength: int = 0,
                 agility: int = 0,
                 vitality: int = 0,
                 resistance: int = 0,
                 dexterity: int = 0,
                 x: int = 0,
                 y: int = 0,
                 x_cp: int = 0,
                 y_cp: int = 0,
                 st_points: int = 0,
                 sk_points: int = 0,
                 slot1: str = "Red Potion",
                 slot2: str = "Litle Red Potion",
                 equip=None,
                 inventory: Inventory = Inventory(),
                 status: int = 0,
                 outside: bool = False,
                 place=None,
                 explored_map: np.array = None,
                 poison: int = 0):

        if len(name) > 12:
            self.name = name
        else:
            self.name = name[:12]

        # Status of player attributes.
        self.hp = hp  # Hit points or life.
        self.hpmax = hpmax  # Max hit points or max life.
        self.lvl = lvl  # Level of player.
        self.exp = exp  # Actual experience points.
        self.expmax = expmax  # Max experience points for level up.
        self.attack = attack  # Current attack of player (base stats + equipment + others).
        self.defense = defense  # Current defense of player (base stats + equipment + others).
        self.evasion = evasion  # Current evasion of player (base stats + equipment + others).
        self.precision = precision  # Current precision of player (base stats + equipment + others).
        self.status = status  # 0: walk, 1: surf.
        self.poison = poison

        # Stats of player attributes.
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
        self.st_points = st_points
        self.sk_points = sk_points

        # Placement player and map attributes.
        self.x = x
        self.y = y
        self.x_cp = x_cp
        self.y_cp = y_cp
        self.outside = outside
        self.place = place

        if explored_map is None:
            self.map = np.zeros(shape=(32, 32, 4), dtype=np.uint8)
            self.map[:, :, 3] = np.ones(shape=(32, 32), dtype=np.uint8) * 255

        # Inventory and equip player attributes.
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
        self.events = {"message": False, "permission": False, "win": False}

        # Other player attributes.
        self.time_played = timedelta(seconds=0)

    def heal(self, amount: int) -> None:
        if self.hp + amount < self.hpmax:
            self.hp += amount

        else:
            self.hp = self.hpmax

    def heal_poisoning(self):
        if self.poison:
            self.poison = 0

    def refresh_time_played(self, time_close: int, time_init: int):
        self.time_played = time_close - time_init + self.time_played

    def refresh_status(self):
        if self.poison > 0:
            self.hp -= self.poison
