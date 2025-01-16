# Imports.
# Local imports.
# External imports.
from attrs import define, field


@define
class Mob:
    # Basics attributes.
    name: str = field(default=None)
    hp: int = field(default=None)
    hpmax: int = field(default=None)
    description: str = field(default="...")

    # Combats attributes.
    attack: int = field(default=0)
    defense: int = field(default=0)
    evasion: float = field(default=0)
    precision: float = field(default=0)

    critical_coeficient: float = field(default=1)
    critical_chance: float = field(default=0)

    poison: int = field(default=0)
    poison_chance: float = field(default=0)

    escape_chance: float = field(default=50)

    hostile: bool = field(default=True)

    # Drop attributes.
    items: dict = field(default=None)
    items_drop_chances: list = field(default=None)
    experience: int = field(default=0)

    # Others.
    escape_mob_probability: float = field(default=0)

    def __attrs_post_init__(self):
        if self.hpmax is None:
            self.hpmax = self.hp
