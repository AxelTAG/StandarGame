# Imports.
# Local imports.
from enums import EntryType, Season

# External imports.
import random
from attrs import define, field


@define
class Biome:
    # Common attributes.
    name: str = field(default="...")
    color: tuple = field(default=(255, 0, 0, 255))
    description: str = field(default="...")
    entries: dict = field(default=None)

    # Mobs and fighting attributes.
    mobs: list = field(default=None)
    mobs_chances: list = field(default=None)
    mobs_respawned: list = field(default=None)
    mobs_respawn_time: int = field(default=8)
    mobs_quantity: int = field(default=3)
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

    # Place climate and bioma attributes.
    altitude: int = field(default=5)
    base_temperature: int = field(default=15)
    season_temperatures: dict = field(default=None)
    water: bool = field(default=False)
    fishs: list = field(default=None)
    fishs_respawned: list = field(default=None)

    def __attrs_post_init__(self):
        if self.entries is None:
            self.entries = {}

        if self.items is None:
            self.items = []

        if self.mobs is None:
            self.mobs = []

        if self.mobs_chances is None:
            self.mobs_chances = []

        if self.mobs_respawned is None:
            self.mobs_respawned = []
            self.respawn_mobs(day=self.mobs_respawn_time)

        if self.npc is None:
            self.npc = []

        if self.req is None:
            self.req = []

        if self.status is None:
            self.status = []

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

    def refresh_temperature(self, season: Season = None) -> None:
        self.base_temperature = self.season_temperatures[season]

    def respawn_mobs(self, day: int) -> None:
        if not bool(self.mobs):
            return

        if len(self.mobs_respawned) >= self.mobs_quantity:
            return

        if day % self.mobs_respawn_time != 0:
            return

        quantity = random.randint(a=len(self.mobs_respawned), b=self.mobs_quantity)

        for _ in range(quantity):
            self.mobs_respawned.extend(random.choices(self.mobs, weights=self.mobs_chances, k=1))

    def has_mob_respawned(self, mob: str) -> bool:
        return mob in self.mobs_respawned

    def refresh_biome(self, day: int, season: Season):
        self.refresh_temperature(season=season)
        self.respawn_mobs(day=day)


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
        if self.entries is None:
            self.entries = {}

        if self.items is None:
            self.items = []

        if self.mobs is None:
            self.mobs = []

        if self.mobs_chances is None:
            self.mobs_chances = []

        if self.npc is None:
            self.npc = []

        if self.req is None:
            self.req = []

        if self.status is None:
            self.status = []

        if self.hide is None:
            self.hide = {"visibility": True, "finding_chance": 0}
