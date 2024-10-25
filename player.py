# Imports.
# Local imports.
from biome import Biome, Entry
from enums import PlayerStatus
from inventory import Inventory

# External imports.
import numpy as np
from attr import define, field
from datetime import timedelta, datetime


# Player class.
@define
class Player:
    # Player name.
    name: str = field(default="")

    # Player current attributes.
    hp: int = field(default=25)  # Hit points or life.
    hpmax: int = field(default=25)  # Max hit points or max life.
    lvl: int = field(default=1)  # Level of player.
    exp: int = field(default=0)  # Actual experience points.
    expmax: int = field(default=10)  # Max experience points for level up.

    attack: int = field(default=2)  # Current attack of player (base stats + equipment + others).
    defense: int = field(default=1)  # Current defense of player (base stats + equipment + others).
    evasion: int = field(default=0)  # Current evasion of player (base stats + equipment + others).
    precision: int = field(default=0)  # Current precision of player (base stats + equipment + others).

    status: int = field(default=PlayerStatus.WALK.value)
    poison: int = field(default=0)

    # Player basis attributes.
    b_hpmax: int = field(default=25)
    b_attack: int = field(default=2)
    b_defense: int = field(default=1)
    b_evasion: float = field(default=0)
    b_precision: float = field(default=0.6)

    # Stats attributes.
    strength: int = field(default=0)
    agility: int = field(default=0)
    vitality: int = field(default=0)
    resistance: int = field(default=0)
    dexterity: int = field(default=0)

    # Player location attributes.
    x: int = field(default=0)
    y: int = field(default=0)
    x_cp: int = field(default=0)
    y_cp: int = field(default=0)
    outside: bool = field(default=False)
    place: Biome | Entry = field(default=None)

    # Lvl up attributes.
    st_points: int = field(default=0)
    sk_points: int = field(default=0)

    # Inventory attributes.
    inventory: Inventory = field(default=None)
    slot1: str = field(default="red_potion")
    slot2: str = field(default="litle_red_potion")
    equip: dict = field(default=None)

    # Map attributes.
    explored_map: np.array = field(default=None)

    # Others.
    events: dict = field(default=None)
    time_played: timedelta = field(default=timedelta(seconds=0))

    def __attrs_post_init__(self):
        if len(self.name) > 12:
            self.name = self.name[:12]

        if self.inventory is None:
            self.inventory = Inventory()

        if self.explored_map is None:
            self.map = np.zeros(shape=(32, 32, 4), dtype=np.uint8)
            self.map[:, :, 3] = np.ones(shape=(32, 32), dtype=np.uint8) * 255

        if self.equip is None:
            self.equip = {"head": "None", "chest": "None", "right_hand": "None", "left_hand": "None", "legs": "None"}

        else:
            # Make sure equip is a dictionary with the correct keys.
            valid_keys = {"head", "chest", "right_hand", "left_hand", "legs"}
            self.equip = {key: self.equip.get(key, "None") for key in valid_keys}

        if self.events is None:
            self.events = {"message": False, "permission": False, "win": False}

    def heal(self, amount: int) -> None:
        if self.hp + amount < self.hpmax:
            self.hp += amount

        else:
            self.hp = self.hpmax

    def heal_poisoning(self):
        if self.poison:
            self.poison = 0

    def refresh_time_played(self, time_close: timedelta | datetime, time_init: timedelta | datetime):
        self.time_played = time_close - time_init + self.time_played

    def refresh_status(self):
        if self.poison > 0:
            self.hp -= self.poison
