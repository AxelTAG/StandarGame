# Imports.
# External imports.
import copy
import random

from attrs import asdict,define, field


@define
class Entitie:
    # Basic attributes.
    name: str = field(default=None)
    description: str = field(default=None)
    id: str = field(default=None)

    # Status attributes.
    visible: bool = field(default=True)
    visibility: float = field(default=1)
    interactable: bool = field(default=False)

    def __attrs_post_init__(self):
        if self.id is None:
            self.id = self.underscores(text=self.name.lower())

    @staticmethod
    def underscores(text: str):
        return text.replace(" ", "_").lower()


@define
class Fish(Entitie):
    # Swim attributes.
    depth: int = field(default=1)
    spawn_months: list[int] = field(default=None)
    catch_chance: float = field(default=0.2)

    # Growth attributes.
    growth_rate: float = field(default=0.001)
    weight: float = field(init=False)
    max_weight: float = field(default=1)
    age: int = field(default=None)
    max_age: int = field(default=24 * 64 * 8)

    # Place attributes.
    movable: bool = field(default=True)
    movable_biomes: list[str] = field(default=None)
    move_chance: float = field(default=0)

    # Data attributes.
    unique_id: str = field(default=None)

    def __attrs_post_init__(self):
        # Super init.
        super().__attrs_post_init__()

        # Swim attributes.
        if self.spawn_months is None:
            self.spawn_months = list(range(8))

        # Growth attributes.
        self.weight = max(min(random.random(), 0.5) * self.max_weight, self.max_weight * 0.2)

        if self.age is None:
            self.age = random.randint(a=0, b=int(0.3 * self.max_age))

        # Basic attributes.
        self.description = f"{self.description}\nWEIGHT: {self.weight:.2f}"

        # Data attributes.
        self.unique_id = f"{self.weight:.2f}"

    # Growth methods.
    def refresh(self, hours: int) -> None:
        self.description = f"{self.description}\nWEIGHT: {self.weight}"
        self.weight += hours * self.growth_rate
        self.age += hours
        self.unique_id = f"{self.weight: .2f}"

    def is_alive(self) -> bool:
        return self.age <= self.max_age

    # Move methods.
    def is_mobile(self) -> bool:
        return self.movable

    def move(self, place) -> bool:
        if self.is_mobile():
            if place.id in self.movable_biomes:
                return True
        return False

    def random_move(self, places: list) -> None:
        if not self.movable_biomes:
            return

        if not self.move_chance > random.random():
            return

        places = list(filter(lambda x: x.id in self.movable_biomes, places))
        if places:
            place = random.choices(places, k=1)[0]
            if self.move(place=place):
                return place
        return

    # Data methods.
    def get_data(self) -> dict:
        return asdict(self, recurse=False)

    # Drop methods.
    def get_drop_item(self, base: dict):
        item = copy.deepcopy(base[self.id])
        item.set_data(data=self.get_data())
        item.update_item_by_data()
        return item


@define
class Tree(Entitie):
    pass


@define
class Butterfly(Entitie):
    pass


@define
class Crab(Entitie):
    pass
