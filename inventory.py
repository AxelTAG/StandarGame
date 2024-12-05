# Imports.
# Local imports.
from globals import ITEMS


class Inventory:
    def __init__(self, items=None, gold: int = 5):
        if items is None:
            items = {"red_potion": 2, "little_red_potion": 2}

        self.items = items
        self.gold = gold

    def add_item(self, item: str, quantity: int) -> bool:
        if item == "gold":
            self.gold += quantity
            return True
        elif item in self.items.keys():
            self.items[item] += quantity
            return True
        elif item != "none":
            self.items[item] = quantity
            return True
        else:
            return False

    def discard_item(self, item: str, quantity: int) -> bool:
        if item in self.items.keys():
            if self.items[item] >= quantity:
                self.items[item] -= int(quantity)
                if self.items[item] == 0:
                    del self.items[item]
                return True
            else:
                return False
        else:
            if item == "gold":
                self.gold -= min([self.gold, quantity])
                return True
            else:
                return False

    def drop_item(self, item: str, quantity: int) -> bool:
        if item in self.items.keys():
            if self.items[item] >= quantity:
                self.items[item] -= int(quantity)
                if self.items[item] == 0:
                    del self.items[item]
                return True
            else:
                return False
        else:
            if item == "gold":
                self.gold -= min([self.gold, quantity])
                return True
            else:
                return False

    @property
    def item_objects(self):
        for item in self.items.keys():
            yield ITEMS[item]
