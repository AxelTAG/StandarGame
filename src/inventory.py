# Imports.
# Local imports.
# External imports.


class Inventory:
    def __init__(self,
                 items=None,
                 gold: int = 5,
                 item_base: dict = None):
        if items is None:
            items = {"red_potion": 2, "little_red_potion": 2}

        self.items = items
        self.gold = gold
        self.item_base = item_base

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
            return False
        else:
            if item == "gold":
                self.gold -= min([self.gold, quantity])
                return True
            return False

    def drop_item(self, item: str, quantity: int) -> bool:
        return self.discard_item(item=item, quantity=quantity)

    @property
    def get_item_objects(self):
        for item in self.items.keys():
            yield self.item_base[item]

    def get_item_object(self, item: str):
        return self.item_base[item]

    def has(self, item: str, amount: int) -> bool:
        if item == "gold":
            return self.gold >= amount
        if item in self.items.keys():
            return self.items[item] >= amount
        return False
