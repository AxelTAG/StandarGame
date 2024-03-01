# Imports.
# External imports.
# Local imports.


# Inventory class.
class Inventory:
    def __init__(self, items=None, gold: int = 5):
        if items is None:
            items = {"red_potion": 2, "litle_red_potion": 2, "short_sword": 1}

        self.items = items
        self.gold = gold
