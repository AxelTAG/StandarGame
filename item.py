# Imports.
# Local imports.
from enums import BodyPart

# External imports.
from attrs import define, field


@define
class Item:
    # Item name.
    name: str = field(default=None)
    description: str = field(default=None)

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

    # Sound attributes.
    tracks: dict = field(default=None)

    def __attrs_post_init__(self):
        if self.tracks is not None:
            for key in range(0, 8):
                self.tracks.setdefault(key, None)

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
