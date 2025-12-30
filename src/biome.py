# Imports.
# Local imports.
from .enums import *
from .mob import Mob
from .entities.entitie import Fish, Tree
from .globals import FISH_RATE_RESPAWN, TREES_RATIO

# External imports.
import copy
import random
from attrs import define, field


# TODO: reemplazar esta función converter por factory de attrs.
def to_default_month_dict(value):
    if value is None:
        return

    if isinstance(value, dict):
        result = {}
        last_value = None
        for i in range(len(Months)):
            if i in value:
                last_value = value[i]
            result[i] = last_value
        return result
    return {month.value: value for month in Months}


def none_to_month_dict_list(value):
    if value is None:
        return {month.value: [] for month in Months}

    if isinstance(value, dict):
        result = {}
        last_value = None
        for i in range(len(Months)):
            if i in value:
                last_value = value[i]
            result[i] = last_value
        return result
    return {month.value: value for month in Months}


@define
class Biome:
    # Common attributes.
    name: dict[int, str] | str = field(default="...", converter=to_default_month_dict)
    color: dict[int, tuple] | tuple = field(default=(255, 0, 0, 255), converter=to_default_month_dict)
    description: dict[int, str] | str = field(default="...", converter=to_default_month_dict)
    entries: dict = field(default=None)
    id: str = field(default=None)
    color_label: tuple = field(default=(255, 0, 0, 255))
    _name: str = field(init=False)
    _color: tuple = field(init=False)
    _description: str = field(init=False)

    # Mobs and fighting attributes.
    mobs: list = field(default=None)
    mobs_names: dict[int, list[str]] | list[str] = field(default=None, converter=none_to_month_dict_list)
    mobs_chances: dict[int, list] | list = field(default=None, converter=none_to_month_dict_list)
    mobs_respawned: list = field(default=None)
    mobs_respawn_time: dict[int, int] | int = field(default=8, converter=to_default_month_dict)
    mobs_check_respawn: bool = field(default=False)
    mobs_quantity: dict[int, int] | int = field(default=3, converter=to_default_month_dict)
    mobs_base: dict = field(default=None)
    fight: bool = field(default=True)
    _mobs_names: list = field(init=False)
    _mobs_chances: list = field(init=False)
    _mobs_respawn_time: int = field(init=False)
    _mobs_quantity: int = field(init=False)

    # Place attributes.
    npcs: list = field(default=None)
    items: list = field(default=None)
    req: dict[int, list] | list = field(default=None, converter=none_to_month_dict_list)
    accessible_from: list[str] = field(default=None)
    accessible_to: list[str] = field(default=None)
    pace: dict[int, int] | int = field(default=8, converter=to_default_month_dict)
    draw_map: bool = field(default=True)
    status: dict[int, list] | list = field(default=[PlayerStatus.WALK.value], converter=none_to_month_dict_list)
    x: int = field(default=None)
    y: int = field(default=None)
    coordinates: tuple[float, float] = field(init=False)
    _req: list = field(init=False)
    _pace: int = field(init=False)
    _status: list = field(init=False)

    # Place climate and bioma attributes.
    altitude: int = field(default=5)
    month_temperatures: dict[int, int] = field(default=15, converter=to_default_month_dict)
    water: dict[int, bool] | bool = field(default=False, converter=to_default_month_dict)
    trees: list[str] = field(default=None)
    trees_ratio: dict = field(default=None)
    trees_respawned: list = field(factory=list)
    trees_quantity: int = field(default=3)
    trees_base: dict = field(default=None)
    fishes: dict[int, list] | list = field(default=None, converter=none_to_month_dict_list)
    fishes_respawned: list = field(factory=list)
    fishes_respawn_time: dict[int, int] = field(default=16, converter=to_default_month_dict)
    fishes_base: dict = field(default=None)
    _temperature: int = field(init=False)
    _water: bool = field(init=False)
    _fishes: list = field(init=False)
    _fishes_respawn_time: int = field(init=False)
    _current_month: int = field(init=False)

    # Reinit attributes.
    reinit_items: dict = field(factory=dict)

    def __attrs_post_init__(self):
        # Common attributes.
        if self.entries is None:
            self.entries = {}

        self._name = self.get_name(month=Months.AURENAR.value)
        self._color = self.get_color(month=Months.AURENAR.value)
        self._description = self.get_description(month=Months.AURENAR.value)

        # Mobs and fighting attributes (Pre).
        self._mobs_names = self.get_mobs_names(month=Months.AURENAR.value)
        self._mobs_chances = self.get_mobs_chances(month=Months.AURENAR.value)
        self._mobs_respawn_time = self.get_mobs_respawn_time(month=Months.AURENAR.value)
        self._mobs_quantity = self.get_mobs_quantity(month=Months.AURENAR.value)

        # Place attributes.
        if self.npcs is None:
            self.npcs = []

        if self.items is None:
            self.items = []

        self.coordinates = (self.x, self.y)

        self._req = self.get_req(month=Months.AURENAR.value)
        self._pace = self.get_pace(month=Months.AURENAR.value)
        self._status = self.get_status(month=Months.AURENAR.value)

        # Place climate and bioma attributes.
        if self.trees_ratio is None and self.trees:
            self.trees_ratio = dict.fromkeys(self.trees, TREES_RATIO)
        self._temperature = self.get_temperature(month=Months.AURENAR.value)
        self._water = self.get_water(month=Months.AURENAR.value)
        self._fishes = self.get_fishes(month=Months.AURENAR.value)
        self._fishes_respawn_time = self.get_fishes_respawn_time(month=Months.AURENAR.value)
        self._current_month = Months.AURENAR.value

        # Fihes.
        self.respawn_fishes(day=self._fishes_respawn_time)

        # Mobs and fighting attributes (Post).
        if self.mobs is None:
            self.set_mobs(list_mob_names=self.mobs_names[Months.AURENAR.value],
                          mob_base=self.mobs_base)

        if self.mobs_chances is None:
            self.mobs_chances = {Months.AURENAR.value: []}

        if self.mobs_respawned is None:
            self.mobs_respawned = []
            self.respawn_mobs(day=self.mobs_respawn_time[Months.AURENAR.value])

        # Reinit attributes.
        if not self.reinit_items:
            self.reinit_items = {}

    @property
    def temperature(self) -> int:
        return self._temperature + self.altitude // 180

    # General get methods.
    def get_name(self, month: int) -> str:
        if month < 0:
            raise ValueError
        return self.name.get(month, self.get_previous_value(data=self.name, key=month))

    def get_color(self, month: int) -> tuple:
        if month < 0:
            raise ValueError
        return self.color.get(month, self.get_previous_value(data=self.color, key=month))

    def get_description(self, month: int) -> str:
        if month < 0:
            raise ValueError
        return self.description.get(month, self.get_previous_value(data=self.description, key=month))

    def get_mobs_names(self, month: int) -> list:
        if month < 0:
            raise ValueError
        return self.mobs_names.get(month, self.get_previous_value(data=self.mobs_names, key=month))

    def get_mobs_chances(self, month: int) -> list:
        if month < 0:
            raise ValueError
        return self.mobs_chances.get(month, self.get_previous_value(data=self.mobs_chances, key=month))

    def get_mobs_respawn_time(self, month: int) -> int:
        if month < 0:
            raise ValueError
        return self.mobs_respawn_time.get(month, self.get_previous_value(data=self.mobs_respawn_time, key=month))

    def get_mobs_quantity(self, month: int) -> int:
        if month < 0:
            raise ValueError
        return self.mobs_quantity.get(month, self.get_previous_value(data=self.mobs_quantity, key=month))

    def get_npc(self) -> list:
        return self.npcs

    def get_items(self) -> list:
        return self.items

    def get_req(self, month: int) -> list:
        if month < 0:
            raise ValueError
        return self.req.get(month, self.get_previous_value(data=self.req, key=month))

    def get_pace(self, month: int) -> int:
        if month < 0:
            raise ValueError
        return self.pace.get(month, self.get_previous_value(data=self.pace, key=month))

    def get_status(self, month: int) -> list:
        if month < 0:
            raise ValueError
        return self.status.get(month, self.get_previous_value(data=self.status, key=month))

    def get_temperature(self, month: int) -> int:
        if month < 0:
            raise ValueError
        return self.month_temperatures.get(month, self.get_previous_value(data=self.month_temperatures, key=month))

    def get_water(self, month: int) -> bool:
        if month < 0:
            raise ValueError
        return self.water.get(month, self.get_previous_value(data=self.water, key=month))

    def get_trees(self) -> list:
        return self.trees

    def get_fishes(self, month: int) -> list:
        if month < 0:
            raise ValueError
        return self.fishes.get(month, self.get_previous_value(data=self.fishes, key=month))

    def get_fishes_respawn_time(self, month: int) -> int:
        if month < 0:
            raise ValueError
        return self.fishes_respawn_time.get(month, self.get_previous_value(data=self.fishes, key=month))

    def is_accessible_from(self, biome: str) -> bool:
        if self.accessible_from is None:
            return True
        return biome in self.accessible_from

    # Place methods.
    def set_x(self, value: int) -> None:
        if isinstance(value, int):
            self.x = value
            self.coordinates = (value, self.coordinates[1])
            return
        raise TypeError

    def set_y(self, value: int) -> None:
        if isinstance(value, int):
            self.y = value
            self.coordinates = (self.coordinates[0], value)
            return
        raise TypeError

    def set_coordinates(self, value: tuple[int, int]) -> None:
        if isinstance(value, tuple):
            if isinstance(value[0], int) and isinstance(value[1], int):
                self.coordinates = value
                raise TypeError
        return

    def is_accessible_to(self, biome: str) -> bool:
        if self.accessible_to is None:
            return True
        return biome in self.accessible_to

    # Mobs methods.
    def has_mob_respawned(self, mob_id: int | str) -> bool:
        if isinstance(mob_id, str):
            for mob in self.mobs_respawned:
                if mob.id_key == mob_id:
                    return True
            return False

        for mob in self.mobs_respawned:
            if mob.id == mob_id:
                return True
        return False

    def reset_mobs(self, force_respawn: bool = False):
        if force_respawn:
            self.mobs_check_respawn = False
        self.discard_mobs()
        self.respawn_mobs(day=self._mobs_respawn_time)

    def respawn_mob(self, mob: str, amount: int = 1) -> None:
        for _ in range(amount):
            self.add_mob_respawned(mob=copy.deepcopy(self.mobs_base[mob]))

    def respawn_mobs(self, day: int) -> None:
        if self.mobs_check_respawn:
            if not day % self._mobs_respawn_time == 0:
                self.mobs_check_respawn = False
            return

        if not bool(self._mobs_names):
            return

        if len(self.mobs_respawned) >= self._mobs_quantity:
            return

        if not day % self._mobs_respawn_time == 0:
            self.mobs_check_respawn = False
            return
        quantity = random.randint(a=len(self.mobs_respawned), b=self._mobs_quantity)

        for _ in range(quantity):
            mob = random.choices(self._mobs_names, weights=self._mobs_chances, k=1)[0]
            self.respawn_mob(mob=mob)
        self.mobs_check_respawn = True

    def get_mobs_respawned(self) -> list[Mob]:
        return self.mobs_respawned

    def get_mob(self, mob_id: int | str) -> Mob:
        for mob in self.mobs_respawned:
            if mob.id == mob_id:
                return mob
            if mob.id_key == mob_id:
                return mob

    def get_mob_quantity(self, mob_id: str = None) -> int:
        if mob_id is None:
            return len(self.mobs_respawned)
        if self.has_mob_respawned(mob_id=mob_id):
            return [mob.id_key for mob in self.mobs_respawned].count(mob_id)
        return 0

    def move_mobs(self, biomes: list):
        for mob in self.mobs_respawned:
            place = mob.random_move(places=biomes)
            if place:
                place.add_mob_respawned(mob=mob)
                self.remove_mob_respawned(mob=mob)

    def add_mob_respawned(self, mob: Mob) -> None:
        if len(self.mobs_respawned) >= self._mobs_quantity:
            return

        self.mobs_respawned.append(mob)

    def remove_mob_respawned(self, mob: Mob = None, mob_id: int = None) -> None:
        if mob:
            if mob in self.mobs_respawned:
                self.mobs_respawned.remove(mob)
            return
        if mob_id:
            for m in self.mobs_respawned:
                if m.id == mob_id:
                    self.mobs_respawned.remove(m)
                    return

    def discard_mobs(self) -> None:
        self.mobs_respawned = []

    def discard_death_mobs(self) -> None:
        for mob in self.mobs_respawned:
            if mob.hp <= 0:
                self.remove_mob_respawned(mob=mob)

    def set_mobs(self,
                 list_mob_names: list[str],
                 mob_base: dict[str, dict]) -> list | None:
        if list_mob_names is None:
            return []

        mobs = []
        for mob in list_mob_names:
            mobs.append(copy.deepcopy(mob_base[mob]))
        self.mobs = mobs

    # Refresh methods.
    def refresh_biome(self, day: int, month: int, neighboors: list, fishes: bool = True) -> None:
        # Update of private attributes.
        self._name = self.get_name(month=month)
        self._color = self.get_color(month=month)
        self._description = self.get_description(month=month)

        self._mobs_names = self.get_mobs_names(month=month)
        self._mobs_chances = self.get_mobs_chances(month=month)
        self._mobs_respawn_time = self.get_mobs_respawn_time(month=month)
        self._mobs_quantity = self.get_mobs_quantity(month=month)

        self._req = self.get_req(month=month)
        self._pace = self.get_pace(month=month)
        self._status = self.get_status(month=month)

        self._temperature = self.get_temperature(month=month)
        self._water = self.get_water(month=month)
        self._fishes = self.get_fishes(month=month)
        self._fishes_respawn_time = self.get_fishes_respawn_time(month=month)

        self._current_month = month

        # Mobs.
        self.discard_death_mobs()
        self.move_mobs(biomes=neighboors)
        self.respawn_mobs(day=day)

        # Fruits.
        self.respawn_fruits(day=day)

        # Fishes.
        if fishes:
            self.respawn_fishes(day=day)

    # Npc methods.
    def add_npc(self, npc: str) -> None:
        if npc in self.npcs:
            return
        self.npcs.append(npc)

    def remove_npc(self, npc: str) -> None:
        self.npcs.remove(npc)

    # Item methods.
    def add_item(self, item_id: str, quantity: int = 1) -> None:
        self.items.extend([item_id] * quantity)

    def remove_item(self, item: str, remove_all: bool = False, player=None) -> None:
        while self.has_item(item_id=item):
            self.items.remove(item)
            if not remove_all:
                return
        if player:
            player.update_quests(target=item, amount=1)

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        return self.items.count(item_id) >= quantity

    # Tree methods.
    def respawn_trees(self, base: dict = None) -> None:
        if base is None:
            base = self.trees_base
        if self.trees is None:
            return

        for tree in random.choices(self.trees, k=random.randint(a=0, b=self.trees_quantity)):
            if self.trees_ratio[tree] <= random.random():
                self.trees_respawned.append(copy.deepcopy(self.trees_base[tree]))

    def get_trees_respawned(self) -> list:
        return self.trees_respawned

    def get_tree_respawned(self, tree_id: str) -> Tree:
        for tree in self.get_trees_respawned():
            if tree.id == tree_id:
                return tree

    def reset_trees_respawned(self) -> None:
        if self.trees is not None:
            self.trees_respawned.clear()
            self.respawn_trees(base=self.trees_base)

    def respawn_fruits(self, day: int, force_respawn: bool = False) -> None:
        for tree in self.trees_respawned:
            if force_respawn:
                self.items.extend(tree.produce_fruit())
                return

            if not day % tree.bearing_frencuency == 0:
                return

            if self._current_month not in tree.bearing_months:
                return

            if tree.fruit in self.items:
                return
            self.items.extend(tree.produce_fruit())

    # Fish methods.
    def get_fishs_respawned(self) -> list:
        return self.fishes_respawned

    def get_fish_quantity(self) -> int:
        return len(self.get_fishs_respawned())

    def add_respawned_fish(self, fish: Fish) -> None:
        self.fishes_respawned.append(fish)

    def remove_respawned_fish(self, fish: Fish) -> None:
        self.fishes_respawned.remove(fish)

    def respawn_fishes(self, day: int, base: dict = None, force_respawn: bool = False) -> None:
        if base is None:
            base = self.fishes_base
        if self.fishes is None:
            return
        if not force_respawn:
            if not day % self._fishes_respawn_time == 0:
                return
        if len(self.fishes_respawned) > 0:
            return

        month = self._current_month
        fishes = self.add_entities_from_base(entities=self.get_fishes(month=month), base=base)
        fish_entities = [fish for fish in fishes if month in fish.spawn_months]
        if fishes:
            if random.random() < FISH_RATE_RESPAWN:
                fishs_to_respawn = random.choices(fish_entities, k=2)
                self.fishes_respawned.extend(fishs_to_respawn)

    def reset_fishes_respawned(self) -> None:
        self.fishes_respawned.clear()
        self.respawn_fishes(day=self._fishes_respawn_time)

    # Reinit methods.
    def has_reinit_items(self) -> bool:
        return bool(self.reinit_items)

    def reinit_items_now(self) -> None:
        if not self.reinit_items:
            return
        for item_id, quantity in self.reinit_items:
            if quantity <= 0:
                if self.has_item(item_id=item_id):
                    self.remove_item(item=item_id, remove_all=True)
            if not self.has_item(item_id=item_id, quantity=quantity):
                difference = quantity - self.items.count(item_id)
                self.add_item(item_id=item_id, quantity=difference)

    # Static methods.
    @staticmethod
    def get_previous_value(data: dict, key):
        if key not in data:
            raise KeyError

        keys = list(data.keys())
        index = keys.index(key)
        prev_key = keys[index - 1] if index > 0 else keys[-1]
        return data[prev_key]

    @staticmethod
    def add_entities_from_base(entities: str | list[str], base: dict) -> list:
        return [copy.deepcopy(base[entitie]) for entitie in entities if entitie in base]


@define
class Entry(Biome):
    # Common attributes.
    entry_type: EntryType = field(default=None)
    leave_entry: Biome = field(default=None)
    hide: dict[str, bool | float] = field(default=None)

    # Place attributes.
    draw_map: bool = field(default=False)
    place: list = field(default=None)

    def __attrs_post_init__(self):
        # Common attributes.
        if self.entries is None:
            self.entries = {}

        self._name = self.get_name(month=Months.AURENAR.value)
        self._color = self.get_color(month=Months.AURENAR.value)
        self._description = self.get_description(month=Months.AURENAR.value)

        # Mobs and fighting attributes (Pre).
        self._mobs_names = self.get_mobs_names(month=Months.AURENAR.value)
        self._mobs_chances = self.get_mobs_chances(month=Months.AURENAR.value)
        self._mobs_respawn_time = self.get_mobs_respawn_time(month=Months.AURENAR.value)
        self._mobs_quantity = self.get_mobs_quantity(month=Months.AURENAR.value)

        # Place attributes.
        if self.npcs is None:
            self.npcs = []

        if self.items is None:
            self.items = []

        self.coordinates = (self.x, self.y)

        self._req = self.get_req(month=Months.AURENAR.value)
        self._pace = self.get_pace(month=Months.AURENAR.value)
        self._status = self.get_status(month=Months.AURENAR.value)

        # Place climate and bioma attributes.
        self._temperature = self.get_temperature(month=Months.AURENAR.value)
        self._water = self.get_water(month=Months.AURENAR.value)
        self._fishes = self.get_fishes(month=Months.AURENAR.value)
        self._fishes_respawn_time = self.get_fishes_respawn_time(month=Months.AURENAR.value)
        self._current_month = Months.AURENAR.value

        # Fihes.
        self.respawn_fishes(day=self._fishes_respawn_time)

        # Mobs and fighting attributes (Post).
        if self.mobs is None:
            self.set_mobs(list_mob_names=self.mobs_names[Months.AURENAR.value],
                          mob_base=self.mobs_base)

        if self.mobs_chances is None:
            self.mobs_chances = {Months.AURENAR.value: []}

        if self.mobs_respawned is None:
            self.mobs_respawned = []
            self.respawn_mobs(day=self.mobs_respawn_time[Months.AURENAR.value])

        # Entry attributes.
        if self.hide is None:
            self.hide = {"visibility": True, "finding_chance": 0}
