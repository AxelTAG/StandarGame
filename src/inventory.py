# Imports.
# Local imports.
from .item import Item

# External imports.
from attrs import define, field


@define
class Inventory:
    items: dict = field(default=None)
    gold: int = field(default=5)
    item_base: dict = field(default=None)
    item_base_original_keys: list = field(init=False)

    def __attrs_post_init__(self):
        if self.items is None:
            self.items = {"red_potion": 2, "little_red_potion": 2}

        self.item_base_original_keys = list(self.item_base.keys())

    def add_item(self, item: Item, quantity: int) -> bool:
        if item.id == "gold":
            self.gold += quantity
            return True
        elif item.id in self.items.keys():
            self.items[item.id] += quantity
            return True
        elif item.id != "none":  # TODO: ver si esta comparación es necesaria.
            self.add_item_to_base(item=item)
            self.items[item.id] = quantity
            return True
        else:
            return False

    def add_item_to_base(self, item: Item) -> None:
        if item.is_unique():
            self.item_base[item.id] = item
        if item.id not in self.item_base_original_keys:
            self.item_base[item.id] = item

    def discard_item(self, item: str, quantity: int) -> bool:
        if item in self.items.keys():
            if self.items[item] >= quantity:
                self.items[item] -= int(quantity)
                if self.items[item] == 0:
                    self.discard_item_from_base(item=item)
                    del self.items[item]
                return True
            return False

        if item == "gold":
            self.gold -= min([self.gold, quantity])
            return True
        return False

    def discard_item_from_base(self, item: str) -> None:
        if item not in self.item_base_original_keys:
            del self.item_base[item]

    def drop_item(self, item: str, quantity: int) -> bool:
        return self.discard_item(item=item, quantity=quantity)

    @property
    def get_item_objects(self):
        for item in self.items.keys():
            yield self.item_base[item]

    def get_item_object(self, item: str):
        if item not in self.item_base.keys():
            return None
        return self.item_base[item]

    def get_item_quantity(self, item: str) -> int:
        if self.has(item=item, amount=1):
            return self.items[item]
        return 0

    def get_gold(self) -> int:
        return self.gold

    def has(self, item: str, amount: int) -> bool:
        if item == "gold":
            return self.gold >= amount
        if item in self.items.keys():
            return self.items[item] >= amount
        return False
