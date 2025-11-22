# Imports.
# Local imports.
from .enums import BodyPart, ItemTypes

# External imports.
from attrs import define, field
from enum import Enum


@define
class Item:
    # Item name.
    name: str = field(default=None)
    description: str = field(default=None)
    id: str = field(default=None)
    item_type: Enum = field(default=None)

    # Item stats.
    attack: int = field(default=0)
    defense: int = field(default=0)
    precision: float = field(default=0)
    evasion: float = field(default=0)
    vision: float = field(default=0)
    weight: float = field(default=0)

    body_part: BodyPart = field(default=None)

    # Items properties.
    pickable: bool = field(default=False)
    consumable: bool = field(default=False)
    equippable: bool = field(default=False)
    droppable: bool = field(default=True)
    edible: bool = field(default=False)
    drinkable: bool = field(default=False)
    expiration: int | None = field(default=None)
    fishing: bool = field(default=False)
    readable: bool = field(default=False)
    unique: bool = field(default=False)

    # Buy/Sell prices.
    buy_price: int = field(default=None)
    sell_price: int = field(default=None)

    # Buy/Sell price factors.
    attack_price_factor: int = field(default=50)
    defense_price_factor: int = field(default=40)
    precision_price_factor: int = field(default=200)
    evasion_price_factor: int = field(default=300)
    deprecator_factor: float = field(default=0.4)
    base_value: int = field(default=0)

    # Crafting attributes.
    crafting_materials: dict = field(default=None)

    # Eating and drinking attributes.
    hungry_refill: int = field(default=0)
    thirsty_refill: int = field(default=0)

    # Fishing attributes.
    depth_range: int = field(default=None)

    # Sound attributes.
    tracks: dict = field(default=None)

    # Read attributes.
    title: str = field(default=None)
    readings: list = field(default=None)

    # Equip attributes.
    slots: int = field(default=0)
    slots_packs: dict = field(factory=dict)

    # Temperature attributes.
    warmness: int = field(default=0)

    # Data attributes.
    data: dict = field(default=None)

    def __attrs_post_init__(self):
        # Item name attributes.
        if self.id is None:
            self.id = self.name.replace(" ", "_").lower()

        # Sound attributes.
        if self.tracks is not None:
            for key in range(0, 8):
                self.tracks.setdefault(key, None)

        # Equip attributes.
        for i in range(self.slots):
            self.slots_packs[i] = None

        # Data attributes.
        if self.data is not None:
            if self.data.get("unique_id", False):
                if self.item_type == ItemTypes.FISH:
                    self.id = f"{self.id}_{self.data['unique_id']}"

    # Property methods.
    def is_unique(self) -> bool:
        return self.unique

    # Buy/Sell methods.
    @property
    def get_buy_price(self):
        attack_value = self.attack * self.attack_price_factor
        defense_value = self.defense * self.defense_price_factor
        precision_value = self.precision * self.precision_price_factor
        evasion_value = self.evasion * self.evasion_price_factor

        return attack_value + defense_value + precision_value + evasion_value + self.base_value

    @property
    def get_sell_price(self):
        return self.get_buy_price * self.deprecator_factor

    # Read methods.
    @property
    def get_title(self):
        if self.title:
            return self.title
        return self.name

    # Slot methods.
    def get_slot_quantity(self) -> int:
        return self.slots

    def get_slot_item(self, slot: int):
        if self.has_slot():
            if 0 <= slot <= self.slots:
                return self.slots_packs[slot]
        return None

    def get_slot_items(self) -> list:
        if self.has_slot():
            return [item for item in self.slots_packs.values() if item is not None]

    def get_first_slot_empty(self) -> int | None:
        for slot, item in self.slots_packs.items():
            if item is None:
                return slot

    def has_slot(self) -> bool:
        if self.slots:
            return True
        return False

    def has_slot_empty(self) -> bool:
        if self.has_slot():
            for slot, item in self.slots_packs.items():
                if item is None:
                    return True
        return False

    def set_slot(self, slot: int, item: str) -> bool:
        if self.is_slot_empty(slot=slot):
            self.slots_packs[slot] = item
            return True
        return False

    def is_slot_empty(self, slot: int) -> bool:
        if self.has_slot:
            if 0 <= slot <= self.slots:
                return self.slots_packs[slot] is None
        return False

    def clear_slot(self, slot: int) -> None:
        if self.has_slot():
            self.slots_packs[slot] = None

    # Temperature methods.
    def get_warmness(self) -> int:
        return self.warmness

    # Data methods.
    def get_unique_id(self) -> str:
        unique_id = self.data.get("unique_id", None)
        if unique_id is not None:
            return f"{self.id}_{unique_id}"
        return self.id

    def set_data(self, data: dict) -> None:
        self.data = data

    def update_item_by_data(self) -> None:
        for k, v in self.data.items():
            if getattr(self, k, None) is not None:
                setattr(self, k, v)
        self.id = self.get_unique_id()
