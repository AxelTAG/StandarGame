# Imports.
# Local imports.
# External imports.
from attrs import define, field


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


@define
class Fish(Entitie):
    # Swim attributes.
    depth: int = field(default=1)

    # Place attributes.
    movable: bool = field(default=True)
    movable_biomes: list[int] = field(default=None)
    move_chance: float = field(default=0)


@define
class Tree(Entitie):
    pass


@define
class Butterfly(Entitie):
    pass


@define
class Crab(Entitie):
    pass
