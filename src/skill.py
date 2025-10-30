# Imports.
# Local imports.
import random

from .enums import EquipCondition, SkillElements, RequirementType

# External imports.
from attrs import field, define


@define
class Skill:
    id: str
    name: str
    description: str
    element: int
    power: int
    cost: int
    type: int
    desviation: int = field(default=1)
    accuracy: float = field(default=1)
    critical_factor: float = field(default=1.4)
    critical_chance: float = field(default=0)
    cooldown: int = field(default=0)
    status_effects: list = field(factory=list)
    status_accuracy: list = field(factory=list)
    scaling: dict = field(factory=dict)
    scaling_critical: dict = field(factory=dict)
    requirements_equip: dict = field(factory=dict)
    requirements_items: dict = field(factory=dict)
    requirement_lvl: int = field(default=0)
    requirements_stats: dict = field(factory=dict)
    tags: list = field(factory=list)

    def __attrs_post_init__(self):
        scaling = {
            "strength": 0,
            "resistance": 0,
            "agility": 0,
            "vitality": 0,
            "hpmax": 0,
            "vitality_energy_max": 0,
            "attack": 0,
            "defense": 0,

        }

        scaling_critical = {
            "critical_strength": 0,
            "critical_resistance": 0,
            "critical_agility": 0,
            "critical_vitality": 0,
        }
        self.normalize_dict(dictionary=self.scaling, normalize_dict=scaling)
        self.normalize_dict(dictionary=self.scaling_critical, normalize_dict=scaling_critical)

    def damage(self, caster) -> int:
        power = random.randint(a=self.power - self.desviation, b=self.power + self.desviation)
        return int(max(0, power + self.scale(caster=caster)))

    def is_critical_hit(self, caster) -> bool:
        critical_chance = min(self.critical_chance + self.scale_critical(caster=caster), 0.95)
        critical = critical_chance >= random.random()
        return critical

    def action(self, caster, target) -> tuple[bool, bool, int, bool, list]:
        fail, avaible, effective_damage, critical, effects = False, False, 0, False, []

        if not caster.precision * self.accuracy * (1 - target.evasion) > random.random():
            fail = True
            return fail, avaible, effective_damage, critical, effects

        if not caster.use_vital_energy(amount=self.cost):
            return fail, avaible, effective_damage, critical, effects

        damage = self.damage(caster=caster) * self.get_type_factor(element=self.element)

        if self.is_critical_hit(caster=caster):
            critical = True
            damage *= self.critical_factor

        if self.status_effects:
            for effect, accuracy in zip(self.status_effects, self.status_accuracy):
                if accuracy >= random.random():
                    effects.append(effect)
                    target.add_status(status=effect)

        effective_damage = int(target.take_damage(damage=int(damage)))

        return fail, avaible, effective_damage, critical, effects

    def scale(self, caster) -> int:
        factor = 0
        for k, v in self.scaling.items():
            if hasattr(caster, k):
                factor += v * getattr(caster, k)
        return factor

    def scale_critical(self, caster) -> float:
        factor = 0
        for k, v in self.scaling_critical.items():
            if hasattr(caster, k):
                factor += v * getattr(caster, k)
        return factor

    def apply_statuses(self, target) -> None:
        for i, status in enumerate(self.status_effects):
            if self.status_accuracy[i] >= random.random():
                target.add_status(status=status)

    def check_requirements(self,
                           caster,
                           level: bool = True,
                           equip: bool = True,
                           items: bool = True,
                           stats: bool = True) -> tuple[bool, int, str]:
        if level:
            if self.requirement_lvl >= caster.level:
                return False, RequirementType.LVL.value, f"lvl {self.requirement_lvl}"

        if equip:
            msg = ""
            not_necessary_conditions = []
            for requirement, condition in self.requirements_equip.items():
                if condition == EquipCondition.NECESSARY.value:
                    if not caster.is_equiped(item=requirement):
                        return False, RequirementType.EQUIP.value, f"{requirement}"
                not_necessary_conditions.append(caster.is_equiped(item=requirement))
                msg += f"{self.underscores(text=requirement, delete=True)}, "
            if not any(not_necessary_conditions):
                return False, RequirementType.EQUIP.value, msg[:-2]

        if items:
            for requirement, quantity in self.requirements_items.items():
                if not caster.has(item=requirement, quantity=quantity):
                    return False, RequirementType.ITEM.value, f"{requirement}"

        if stats:
            for requirement, quantity in self.requirements_stats.items():
                if getattr(caster, requirement) >= quantity:
                    return False, RequirementType.STATS.value, f"{requirement}"

        return True, RequirementType.ALL_PAST.value, "all past"

    @staticmethod
    def get_type_factor(element: int) -> float:
        return 1

    @staticmethod
    def normalize_dict(dictionary: dict, normalize_dict: dict) -> None:
        for k, v in normalize_dict.items():
            if k in dictionary.keys():
                continue
            dictionary[k] = v

    @staticmethod
    def underscores(text: str, delete: bool = False) -> str:
        if delete:
            return text.replace("_", " ").lower()
        return text.replace(" ", "_").lower()
