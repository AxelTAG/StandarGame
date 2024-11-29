# Imports.
# Local imports.
from enums import EntryType, Season

# External imports.
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

    # Place climate attributes.
    temperature: int = field(default=15)

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

    def refresh_temperature(self, season: Season = None):
        pass


@define
class Entry(Biome):
    # Common attributes.
    entry_type: EntryType = field(default=None)
    leave_entry: Biome = field(default=None)
    hide: dict[str, bool | float] = field(default=None)

    # Place attributes.
    draw_map: bool = field(default=False)

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
