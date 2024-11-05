# Imports.
# Local imports.
from enums import EntryType, Season


# Biome class.
class Biome:
    def __init__(self,
                 color: tuple = (255, 0, 0, 255),
                 description: str = "...",
                 entries: dict = None,
                 fight: bool = True,
                 items: list = None,
                 mobs: list = None,
                 mobs_chances: list = None,
                 name: str = "...",
                 npc: list = None,
                 req: list = None,
                 pace: int = 8,
                 status: list = None,
                 temperature: int = 15):

        if entries is None:
            entries = {}

        if items is None:
            items = []

        if mobs is None:
            mobs = []

        if mobs_chances is None:
            mobs_chances = []

        if npc is None:
            npc = []

        if req is None:
            req = []

        if status is None:
            status = []

        self.color = color
        self.description = description
        self.entries = entries
        self.fight = fight
        self.items = items
        self.mobs = mobs
        self.mobs_chances = mobs_chances
        self.name = name
        self.npc = npc
        self.req = req
        self.pace = pace
        self.status = status
        self.temperature = temperature

    def refresh_temperature(self, season: Season = None):
        pass


class Entry(Biome):
    def __init__(self,
                 color: tuple = (255, 0, 0, 255),
                 description: str = "...",
                 entries=None,
                 entry_type: EntryType = None,
                 fight: bool = False,
                 items: list = None,
                 leave_entry: Biome = None,
                 mobs: list = None,
                 mobs_chances: list = None,
                 name: str = "...",
                 npc: list = None,
                 req: list = None,
                 status: int = None,
                 hide: tuple[bool, float] = None):

        super().__init__(color, description, entries, fight, items, mobs, mobs_chances, name, npc, req, status)

        self.entry_type = entry_type
        self.hide = hide
        self.leave_entry = leave_entry
