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
    attack: int = field(default=None)
    defense: int = field(default=None)
    precision: float = field(default=None)
    evasion: float = field(default=None)

    body_part: BodyPart = field(default=None)

    # Items properties.
    pickable: bool = field(default=False)
    consumable: bool = field(default=False)
    equippable: bool = field(default=False)
    expiration: int | None = field(default=None)

    # Buy/Sell prices.
    buy_price: int = field(default=None)
    sell_price: int = field(default=None)

    def __attrs_post_init__(self):
        pass
