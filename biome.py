# Imports.
# External imports
# Local imports.


# Biome class.
class Biome:
    def __init__(self,
                 color: tuple = (255, 0, 0, 255),
                 description: str = "...",
                 entries=None,
                 fight: bool = True,
                 items=None,
                 mobs="",
                 mobs_chances=None,
                 name: str = "...",
                 npc=None,
                 req=None,
                 status=None):

        if entries is None:
            entries = {}

        if items is None:
            items = []

        if mobs_chances is None:
            mobs_chances = [0]

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
        self.status = status


class Entry(Biome):
    def __init__(self,
                 color: tuple = (255, 0, 0, 255),
                 description: str = "...",
                 entries=None,
                 fight: bool = False,
                 items=None,
                 leave_entry=Biome,
                 mobs=None,
                 mobs_chances=None,
                 name: str = "...",
                 npc=None,
                 req=None,
                 status: int = 0):

        super().__init__(color, description, entries, fight, items, mobs, mobs_chances, name, npc, req, status)

        self.leave_entry = leave_entry
