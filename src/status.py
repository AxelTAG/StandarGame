# Imports.
# Local imports.
from .enums import StatusType

# External imports.
from attrs import define, field
from enum import Enum


def to_list(value) -> list:
    if isinstance(value, list):
        return value
    return [value]


@define
class Buff:
    name: str = field(factory=str)
    id: str = field(default=None)
    stat: str | list[str] = field(factory=list, converter=to_list)
    amount: float | list[float] = field(default=1, converter=to_list)
    duration: int = field(default=1)
    description: str = field(factory=str)
    source: str = field(factory=str)

    on_apply = field(default=None)
    on_expire = field(default=None)

    def __attrs_post_init__(self):
        if self.id is None:
            self.id = self.name.replace(" ", "_").lower()

    def tick(self, entity):
        if self.on_apply:
            self.on_apply(entity, self)
        self.duration -= 1

    def apply(self, entitie):
        """Applies the buff to the player."""
        for stat, amount in zip(self.stat, self.amount):
            if hasattr(entitie, stat):
                current_value = getattr(entitie, stat)
                setattr(entitie, stat, current_value + amount)
            if self.on_apply:
                self.on_apply(entitie, self)

    def expire(self, entitie):
        """Reverses the buff effect."""
        for stat, amount in zip(self.stat, self.amount):
            if hasattr(entitie, stat):
                current_value = getattr(entitie, stat)
                setattr(entitie, stat, current_value - amount)
            if self.on_expire:
                self.on_expire(entitie, self)

    def is_active(self) -> bool:
        """Returns True if the buff is still active."""
        return self.duration > 0


@define
class Status:
    name: str = field(factory=str)
    duration: int = field(default=1)  # Ticks/Turns.
    stacks: int = field(default=1)
    max_stacks: int = field(default=1)
    priority: int = field(default=0)
    source: str = field(default=None)
    status_type: Enum = field(default=None)

    damaging: bool = field(default=True)
    stunner: bool = field(default=False)
    paralyzer: bool = field(default=False)

    on_apply = field(default=None)
    on_tick = field(default=None)
    on_expire = field(default=None)

    def tick(self, entity):
        if self.on_tick:
            self.on_tick(entity, self)
        self.duration -= 1

    def apply_stack(self, other):
        """Combines other status with same type"""
        self.max_stacks = max(self.max_stacks, other.max_stacks)
        self.stacks = min(self.max_stacks, self.stacks + other.stacks)
        # Refresh of duration.
        self.duration = max(self.duration, other.duration)

    def is_damaging(self) -> bool:
        return self.damaging

    def is_sttuner(self) -> bool:
        return self.stunner

    def is_paralyzer(self) -> bool:
        return self.paralyzer

    @classmethod
    def gen_poison(cls,
                   duration: int,
                   stacks: int,
                   max_stacks: int,
                   source: str):
        return cls(
            status_type=StatusType.POISON,
            name="Poison",
            duration=duration,
            stacks=stacks,
            max_stacks=max_stacks,
            priority=1,
            source=source,
            damaging=True,
            stunner=False,
            paralyzer=False,
        )

    @classmethod
    def gen_freeze(cls,
                   duration: int,
                   stacks: int,
                   max_stacks: int,
                   source: str):
        return cls(
            status_type=StatusType.FREEZE,
            name="Freeze",
            duration=duration,
            stacks=stacks,
            max_stacks=max_stacks,
            priority=1,
            source=source,
            damaging=True,
            stunner=False,
            paralyzer=False,
        )

    @classmethod
    def gen_burn(cls,
                 duration: int,
                 stacks: int,
                 max_stacks: int,
                 source: str):
        return cls(
            status_type=StatusType.BURN,
            name="Burn",
            duration=duration,
            stacks=stacks,
            max_stacks=max_stacks,
            priority=1,
            source=source,
            damaging=True,
            stunner=False,
            paralyzer=False,
        )

    @classmethod
    def gen_stun(cls,
                 duration: int,
                 stacks: int,
                 max_stacks: int,
                 source: str):
        return cls(
            status_type=StatusType.STUN,
            name="Stun",
            duration=duration,
            stacks=stacks,
            max_stacks=max_stacks,
            priority=1,
            source=source,
            damaging=False,
            stunner=True,
            paralyzer=False,
        )

    @classmethod
    def gen_bleed(cls,
                  duration: int,
                  stacks: int,
                  max_stacks: int,
                  source: str):
        return cls(
            status_type=StatusType.BLEED,
            name="Bleed",
            duration=duration,
            stacks=stacks,
            max_stacks=max_stacks,
            priority=1,
            source=source,
            damaging=True,
            stunner=False,
            paralyzer=False,
        )

    @classmethod
    def gen_paralyze(cls,
                     duration: int,
                     stacks: int,
                     max_stacks: int,
                     source: str):
        return cls(
            status_type=StatusType.PARALYSIS,
            name="Paralize",
            duration=duration,
            stacks=stacks,
            max_stacks=max_stacks,
            priority=1,
            source=source,
            damaging=False,
            stunner=False,
            paralyzer=True,
        )
