# Imports.
# Local imports.
# External imports.
import random

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
    visibility: float = field(default=1)

    # Drop attributes.
    items: dict = field(default=None)
    items_drop_chances: list = field(default=None)
    experience: int = field(default=0)

    # Others.
    escape_mob_probability: float = field(default=0)

    def __attrs_post_init__(self):
        if self.hpmax is None:
            self.hpmax = self.hp

    def is_visible(self) -> bool:
        return random.random() >= self.visibility

    def get_drop_odds(self, desired_odds: list = None, drop_len: int = None) -> list:
        if desired_odds is None:
            desired_odds = self.items_drop_chances

        if drop_len is None:
            drop_len = len(desired_odds)

        if drop_len == 0:
            return []

        if drop_len == 1:
            return desired_odds

        odds = []
        for odd in desired_odds:
            odds.append(1 / ((1 / (odd / (drop_len - 1))) / drop_len))
        return odds

    def drop_items(self) -> list:
        quantity = random.randint(a=1, b=len(self.items)) - 1
        items = list(set(random.choices(population=[*self.items.keys()],
                                        cum_weights=self.get_drop_odds(),
                                        k=quantity)))

        return items
