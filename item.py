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

    body_part: BodyPart = field(default=None)

    # Items properties.
    pickable: bool = field(default=False)
    consumable: bool = field(default=False)
    equippable: bool = field(default=False)
    droppable: bool = field(default=True)
    expiration: int | None = field(default=None)

    # Buy/Sell prices.
    buy_price: int = field(default=None)
    sell_price: int = field(default=None)

    def __attrs_post_init__(self):
        pass
