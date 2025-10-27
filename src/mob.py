# Imports.
# Local imports.
from .skill import Skill
from .status import Status

# External imports.
import copy
import random

from attrs import define, field


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

    # Place attributes.
    movable: bool = field(default=True)
    movable_biomes: list[int] = field(default=None)
    move_chance: float = field(default=0)

    # Statuses attributes.
    stun: bool = field(default=False)
    paralyze: bool = field(default=False)
    statuses: list[Status] = field(factory=list)
    statuses_save: list[Status] = field(factory=list)

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

    def is_alive(self) -> bool:
        return self.hp > 0

    # Statuses methods.
    def add_status(self, status: Status) -> None:
        if status is Status:
            self.statuses.append(copy.deepcopy(status))

    def discard_status(self, status: Status) -> None:
        self.statuses.remove(status)

    def is_visible(self) -> bool:
        return random.random() >= self.visibility

    def is_stun(self) -> bool:
        return self.stun

    def is_paralyze(self) -> bool:
        return self.paralyze

    def set_stun(self, value) -> None:
        if value is bool:
            self.stun = value

    def refresh_status(self, onbattle: bool = False) -> None:
        for status in self.statuses:
            if status.damaging:
                self.hp -= status.stacks
            if status.stunner:
                self.set_stun(value=True)
            status.tick(entity=self)
            if status.stacks <= 0:
                self.discard_status(status=status)

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

    def attack_to(self, target) -> tuple[bool, bool, int, bool, list]:
        skill = self.get_standar_attack()
        return skill.action(caster=self, target=target)

    def take_damage(self, damage: int) -> int:
        efective_dmg = max(0, damage - self.defense)
        self.hp = max(0, self.hp - efective_dmg)
        return efective_dmg

    @staticmethod
    def underscores(text: str):
        return text.replace(" ", "_").lower()
