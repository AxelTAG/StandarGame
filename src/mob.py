# Imports.
# Local imports.
from .skill import Skill
from .status import Status

# External imports.
import copy
import random

from attrs import define, field
from enum import Enum


@define
class Mob:
    # Basics attributes.
    name: str = field(default=None)
    hp: int = field(default=None)
    hpmax: int = field(default=None)
    vital_energy: int = field(default=0)
    vital_energy_max: int = field(default=0)
    description: str = field(default="...")
    id: int = field(default=None)
    id_key: str = field(default=None)

    # Lvl attributes.
    level: int = field(default=None)

    # Place attributes.
    movable: bool = field(default=True)
    movable_biomes: list[int] = field(default=None)
    move_chance: float = field(default=0)

    # Statuses attributes.
    stun: bool = field(default=False)
    paralyze: bool = field(default=False)
    statuses: list[Status] = field(factory=list)
    statuses_pre: list[Status] = field(factory=list)
    statuses_saved: list[Status] = field(factory=list)

    # Combats attributes.
    attack: int = field(default=0)
    defense: int = field(default=0)
    evasion: float = field(default=0)
    precision: float = field(default=0)

    critical_coeficient: float = field(default=1)
    critical_chance: float = field(default=0)

    poison_duration: int = field(default=0)
    poison_stacks: int = field(default=0)
    poison_max_stacks: int = field(default=0)
    poison_source: str = field(default=None)
    poison_chance: float = field(default=0)

    escape_chance: float = field(default=50)

    hostile: bool = field(default=True)
    agression: float = field(default=0.4)
    visibility: float = field(default=1)

    # Drop attributes.
    items: dict = field(default=None)
    items_drop_chances: list = field(default=None)
    experience: int = field(default=0)

    # Fighting attributes.
    speed: float = field(default=1)

    # Skills.
    skills: list = field(factory=list)

    # Others.
    escape_mob_probability: float = field(default=0)

    def __attrs_post_init__(self):
        # Basics attributes.
        if self.hpmax is None:
            self.hpmax = self.hp

        if self.vital_energy_max is None:
            self.vital_energy_max = self.vital_energy

        if self.id_key is None:
            self.id_key = self.underscores(text=self.name.lower())

    # Current status methods.
    def has_vital_energy(self) -> bool:
        if hasattr(self, "vital_energy"):
            if self.vital_energy > 0:
                return True
        return False

    def use_vital_energy(self, amount: int) -> bool:
        if self.vital_energy >= amount:
            self.vital_energy -= amount
            return True
        return False

    def is_alive(self, limit: int = 0) -> bool:
        return self.hp > limit

    # Statuses methods.
    def add_status(self, status: Status, onbattle: bool = False) -> None:
        # if onbattle:
        #     self.add_pre_status(status=status)
        #     return
        active_status = self.get_status(status_type=status.status_type)
        if active_status is not None:
            active_status.apply_stack(other=status)
            return
        self.statuses.append(copy.deepcopy(status))

    def add_status_saved(self, status: Status) -> None:
        self.statuses_saved.append(status)

    def add_pre_status(self, status: Status):
        self.statuses_pre.append(copy.deepcopy(status))

    def discard_status(self, status: Status) -> None:
        self.statuses.remove(status)

    def discard_pre_status(self) -> None:
        self.statuses_pre.clear()

    def clear_statuses_saved(self) -> None:
        self.statuses_saved.clear()

    def get_status(self, status_type: Enum) -> Status | None:
        for status in self.statuses:
            if status_type == status.status_type:
                return status

    def is_visible(self) -> bool:
        return random.random() >= self.visibility

    def is_stun(self) -> bool:
        return self.stun

    def is_paralyze(self) -> bool:
        return self.paralyze

    def set_stun(self, value: bool) -> None:
        if isinstance(value, bool):
            self.stun = value
            return
        raise ValueError("Value must be bool.")

    def set_paralyze(self, value: bool) -> None:
        if isinstance(value, bool):
            self.paralyze = value
            return
        raise ValueError("Value must be bool.")

    def apply_status_effects(self, status: Status, tick: bool = True) -> None:
        if status.is_sttuner():
            self.set_stun(value=True)
        if status.is_paralyzer():
            self.set_paralyze(value=True)
        if tick:
            if status.is_damaging():
                self.hp -= status.stacks
            status.tick(entity=self)
            if status.duration <= 0:
                self.statuses.remove(status)
                self.add_status_saved(status=status)

    def refresh_status(self, onbattle: bool = False) -> None:
        self.set_stun(value=False)
        self.set_paralyze(value=False)
        self.clear_statuses_saved()
        for status in self.statuses:
            self.apply_status_effects(status=status, tick=True)

        if not onbattle:
            pass

        # for status in self.statuses_pre:
        #     self.add_status(status=status)
        #     self.apply_status_effects(status=status, tick=False)
        # self.discard_pre_status()

    # Item methods.
    def get_experience(self) -> int:
        return self.experience

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
        if self.items is None:
            return []
        quantity = random.randint(a=0, b=len(self.items))
        items = list(set(random.choices(population=[*self.items.keys()],
                                        cum_weights=self.get_drop_odds(),
                                        k=quantity)))

        return items

    # Place attributes.
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

    # Skill methods.
    def is_skill_available(self, skill: Skill) -> bool:
        if self.vital_energy >= skill.cost:
            return True
        return False

    # Fighting methods.
    def get_standar_attack(self) -> Skill:
        for skill in self.skills:
            if skill.id == "mob_attack":
                return skill

    def attack_to(self, target, onbattle: bool = False) -> tuple[bool, bool, int, bool, list]:
        skill = self.get_standar_attack()
        return skill.action(caster=self, target=target, onbattle=onbattle)

    def take_damage(self, damage: int) -> int:
        efective_dmg = max(0, damage - self.defense)
        self.hp = max(0, self.hp - efective_dmg)
        return efective_dmg

    def should_attack(self, player) -> bool:
        if not self.hostile:
            return False

        if player.presence / 100 * self.agression > random.random():
            return True

    @staticmethod
    def underscores(text: str):
        return text.replace(" ", "_").lower()
