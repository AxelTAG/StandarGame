# Imports.
# Local imports.
from biome import Biome, Entry
from enums import BodyPart, PlayerStatus
from inventory import Inventory
from item import Item

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
    lvl: int = field(default=1)  # Level of player.
    exp: int = field(default=0)  # Actual experience points.
    expmax: int = field(default=10)  # Max experience points for level up.

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
    resistance: int = field(default=0)
    agility: int = field(default=0)
    vitality: int = field(default=0)
    dexterity: int = field(default=0)
    attack_factor: float = field(default=0.4)
    defence_factor: float = field(default=0.4)
    evasion_factor: float = field(default=0.01)
    precision_factor: float = field(default=0.005)
    vitality_factor: float = field(default=1)
    vision: int = field(default=1)

    # Player location attributes.
    x: int = field(default=0)
    y: int = field(default=0)
    x_cp: int = field(default=0)
    y_cp: int = field(default=0)
    outside: bool = field(default=False)
    place: Biome | Entry = field(default=None)
    last_place: Biome | Entry = field(default=None)
    last_entry: Entry = field(default=None)

    # Lvl up attributes.
    st_points: int = field(default=0)
    sk_points: int = field(default=0)

    # Inventory attributes.
    inventory: Inventory = field(default=None)
    slot1: str = field(default="red_potion")
    slot2: str = field(default="litle_red_potion")
    equip: dict = field(default=None)

    # Map attributes.
    map: np.array = field(default=None)

    # Others.
    events: dict = field(default=None)
    time_played: timedelta = field(default=timedelta(seconds=0))

    def __attrs_post_init__(self):
        if len(self.name) > 12:
            self.name = self.name[:12]

        if self.inventory is None:
            self.inventory = Inventory()

        if self.map is None:
            self.map = np.zeros(shape=(32, 32, 4), dtype=np.uint8)
            self.map[:, :, 3] = np.ones(shape=(32, 32), dtype=np.uint8) * 255

        if self.equip is None:
            self.equip = {BodyPart.HEAD: None,
                          BodyPart.CHEST: None,
                          BodyPart.RIGHT_HAND: None,
                          BodyPart.LEFT_HAND: None,
                          BodyPart.LEGS: None}

        else:
            # Make sure equip is a dictionary with the correct keys.
            valid_keys = set(BodyPart)
            self.equip = {key: self.equip.get(key) for key in valid_keys}

        if self.events is None:
            self.events = {"message": False,
                           "permission": False,
                           "win": False,
                           "goblin_chief_crown": False,
                           "message_maisie": False}

    @property
    def attack(self) -> int:
        item_attack_sum = sum(item.attack for item in self.equip.values() if isinstance(item, Item))
        return int(self.b_attack + self.strength * self.attack_factor + item_attack_sum)

    @property
    def defense(self) -> int:
        item_defense_sum = sum(item.defense for item in self.equip.values() if isinstance(item, Item))
        return int(self.b_defense + self.resistance * self.defence_factor + item_defense_sum)

    @property
    def evasion(self) -> float:
        item_evasion_sum = sum(item.evasion for item in self.equip.values() if isinstance(item, Item))
        return self.b_evasion + self.agility * self.evasion_factor + item_evasion_sum

    @property
    def precision(self) -> float:
        item_evasion_sum = sum(item.precision for item in self.equip.values() if item is Item)
        return self.b_precision + self.agility * self.precision_factor + item_evasion_sum

    @property
    def hpmax(self) -> int:
        return int(self.b_hpmax + self.vitality * self.vitality_factor)

    @property
    def exploration_radius(self):
        return self.vision + sum([item.vision for item in self.inventory.item_objects])

    def heal(self, amount: int) -> None:
        if self.hp + amount < self.hpmax:
            self.hp += amount

        else:
            self.hp = self.hpmax

    def heal_poisoning(self) -> None:
        if self.poison:
            self.poison = 0

    def refresh_time_played(self, time_close: timedelta | datetime, time_init: timedelta | datetime) -> None:
        self.time_played = time_close - time_init + self.time_played

    def refresh_status(self) -> None:
        if self.poison > 0:
            self.hp -= self.poison

    def equip_item(self, item: Item) -> None:
        if item.equippable and self.equip[item.body_part] is None:
            self.equip[item.body_part] = item

    def unequip_item(self, item: Item) -> None:
        if item in self.equip.values():
            self.equip[item.body_part] = None

    def add_exp(self, amount: int) -> bool:
        self.exp += amount

        if self.exp >= self.expmax:
            self.lvl_up()
            return True
        else:
            return False

    def lvl_up(self) -> None:
        self.lvl += 1
        self.exp = 0
        self.expmax = 10 * self.lvl
        self.st_points += 3

        self.b_hpmax += 2
        self.b_attack += 0.4
        self.b_defense += 0.20
        self.b_precision += 0.005
        self.b_evasion += 0.01

    def set_place(self, place: Biome | Entry) -> None:
        if type(self.place) == Entry:
            self.last_entry = self.place
        self.last_place = self.place
        self.place = place

    def has(self, item: str) -> bool:
        return item in self.inventory.items.keys() and self.inventory.items[item] >= 0
