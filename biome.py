# Imports.
# Local imports.
from enums import *
from mob import Mob

# External imports.
import copy
import random
from attrs import define, field


@define
class Biome:
    # Common attributes.
    name: str = field(default="...")
    color: tuple = field(default=(255, 0, 0, 255))
    description: str = field(default="...")
    entries: dict = field(default=None)
    id: int = field(default=None)

    # Mobs and fighting attributes.
    mobs: list = field(default=None)
    mobs_names: list[str] = field(default=None)
    mobs_chances: list = field(default=None)
    mobs_respawned: list = field(default=None)
    mobs_respawn_time: int = field(default=8)
    mobs_check_respawn: bool = field(default=False)
    mobs_quantity: int = field(default=3)
    mobs_base: dict = field(default=None)
    fight: bool = field(default=True)

    # Place attributes.
    npc: list = field(default=None)
    items: list = field(default=None)
    req: list = field(default=None)
    pace: int = field(default=8)
    draw_map: bool = field(default=True)
    status: list = field(default=None)
    x: int = field(default=None)
    y: int = field(default=None)
    coordinates: tuple[float, float] = field(init=False)

    # Place climate and bioma attributes.
    altitude: int = field(default=5)
    base_temperature: int = field(default=15)
    season_temperatures: dict = field(default=None)
    water: bool = field(default=False)
    fishs: list = field(default=None)
    fishs_respawned: list = field(default=None)

    def __attrs_post_init__(self):
        # Common attributes.
        if self.entries is None:
            self.entries = {}

        if self.items is None:
            self.items = []

        # Mobs and fighting attributes.
        if self.mobs is None:
            self.set_mobs(list_mob_names=self.mobs_names,
                          mob_base=self.mobs_base)

        if self.mobs_chances is None:
            self.mobs_chances = []

        if self.mobs_respawned is None:
            self.mobs_respawned = []
            self.respawn_mobs(day=self.mobs_respawn_time)

        # Place attributes.
        if self.npc is None:
            self.npc = []

        if self.req is None:
            self.req = []

        if self.status is None:
            self.status = []

        self.coordinates = (self.x, self.y)

        # Place climate and bioma attributes.
        if self.season_temperatures is None:
            self.season_temperatures = {
                Season.SPRING: 20,
                Season.SUMMER: 30,
                Season.AUTUMN: 15,
                Season.WINTER: 5
            }

    @property
    def temperature(self) -> int:
        return self.base_temperature + self.altitude // 180

    def has_mob_respawned(self, mob_id: int) -> bool:
        for mob in self.mobs_respawned:
            if mob.id == mob_id:
                return True
        return False

    def refresh_temperature(self, season: Season = None) -> None:
        self.base_temperature = self.season_temperatures[season]

    def reset_mobs(self, force_respawn: bool = False):
        if force_respawn:
            self.mobs_check_respawn = False
        self.discard_mobs()
        self.respawn_mobs(day=self.mobs_respawn_time)

    def repawn_mob(self, mob: str) -> None:
        self.add_mob_respawned(mob=copy.deepcopy(self.mobs_base[mob]))

    def respawn_mobs(self, day: int) -> None:
        if self.mobs_check_respawn:
            return

        if not bool(self.mobs_names):
            return

        if len(self.mobs_respawned) >= self.mobs_quantity:
            return

        if not day % self.mobs_respawn_time == 0:
            self.mobs_check_respawn = False
            return

        quantity = random.randint(a=len(self.mobs_respawned), b=self.mobs_quantity)

        for _ in range(quantity):
            mob = random.choices(self.mobs_names, weights=self.mobs_chances, k=1)[0]
            self.repawn_mob(mob=mob)
        self.mobs_check_respawn = True

    def move_mobs(self, biomes: list):
        for mob in self.mobs_respawned:
            place = mob.random_move(places=biomes)
            if place:
                place.add_mob_respawned(mob=mob)
                self.remove_mob_respawned(mob=mob)

    def add_mob_respawned(self, mob: Mob) -> None:
        if len(self.mobs_respawned) >= self.mobs_quantity:
            return

        self.mobs_respawned.append(mob)

    def remove_mob_respawned(self, mob: Mob = None, mob_id: int = None) -> None:
        if mob:
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

    def refresh_biome(self, day: int, season: Season, neighboors: list) -> None:
        self.refresh_temperature(season=season)
        self.discard_death_mobs()
        self.move_mobs(biomes=neighboors)
        self.respawn_mobs(day=day)

    def get_mob(self, mob_id: int) -> Mob:
        for mob in self.mobs_respawned:
            if mob.id == mob_id:
                return mob

    def set_mobs(self, list_mob_names: list[str], mob_base: dict[str, dict]) -> list | None:
        if list_mob_names is None:
            return []

        mobs = []
        for mob in list_mob_names:
            mobs.append(copy.deepcopy(mob_base[mob]))
        self.mobs = mobs

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

        if self.items is None:
            self.items = []

        # Mobs and fighting attributes.
        if self.mobs is None:
            self.mobs = []

        if self.mobs_chances is None:
            self.mobs_chances = []

        # Place attributes.
        if self.npc is None:
            self.npc = []

        if self.req is None:
            self.req = []

        if self.status is None:
            self.status = []

        self.coordinates = (self.x, self.y)

        if self.hide is None:
            self.hide = {"visibility": True, "finding_chance": 0}
