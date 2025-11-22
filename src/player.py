# Imports.
# Local imports.
import copy

from .biome import Biome, Entry
from .enums import Actions, BodyPart, PlayerStatus, ObjectiveType, RequirementType, StatusType
from .globals import MAP_X_LENGTH, MAP_Y_LENGTH
from .skill import Skill
from .inventory import Inventory
from .item import Item
from .status import Buff, Status
from .quest import Quest

# External imports.
import random
import numpy as np
from attr import define, field
from datetime import timedelta, datetime
from enum import Enum


# Player class.
@define
class Player:
    # Player name.
    name: str = field(default="")

    # Player current attributes.
    hp: int = field(default=25)  # Hit points or life.
    level: int = field(default=1)  # Level of player.
    exp: int = field(default=0)  # Actual experience points.
    expmax: int = field(default=10)  # Max experience points for level up.
    vital_energy: int = field(default=5)

    # Player basis attributes.
    b_hpmax: int = field(default=25)
    b_vital_energy: int = field(default=5)
    b_attack: int = field(default=2)
    b_defense: int = field(default=1)
    b_evasion: float = field(default=0)
    b_precision: float = field(default=0.6)
    b_weight_carry: float = field(default=5)

    # Stats attributes.
    strength: int = field(default=0)
    resistance: int = field(default=0)
    agility: int = field(default=0)
    vitality: int = field(default=0)
    dexterity: int = field(default=0)
    vision: int = field(default=1)
    perception: int = field(default=0)
    presence: int = field(default=100)

    attack_factor: float = field(default=0.4)
    defence_factor: float = field(default=0.4)
    evasion_factor: float = field(default=0.01)
    precision_factor: float = field(default=0.005)
    vitality_factor: float = field(default=1)
    vital_energy_factor: float = field(default=0.5)

    # Buff attributes.
    buffs: list[Buff] = field(factory=list)
    buffs_applied: list[Buff] = field(factory=list)

    # Status attributes.
    statuses: list[Status] = field(factory=list)
    statuses_save: list[Status] = field(factory=list)

    hungry: int = field(default=100)
    thirsty: int = field(default=100)
    status: int = field(default=PlayerStatus.WALK.value)

    poison: bool = field(default=False)
    freeze: bool = field(default=False)
    burn: bool = field(default=False)
    stun: bool = field(default=False)
    bleed: bool = field(default=False)
    paralyze: bool = field(default=False)

    resistance_poison: float = field(default=0)
    resistance_freeze: float = field(default=0)
    resistance_burn: float = field(default=0)
    resistance_stun: float = field(default=0)
    resistance_bleed: float = field(default=0)
    resistance_paralyze: float = field(default=0)

    # Temperature attributes.
    temperature: int = field(default=36)

    # Player location attributes.
    x: int = field(default=12)
    y: int = field(default=24)
    x_cp: int = field(default=12)
    y_cp: int = field(default=24)
    outside: bool = field(default=False)
    place: Biome | Entry = field(default=None)
    last_place: Biome | Entry = field(default=None)
    last_entry: Entry = field(default=None)
    standing: bool = field(default=True)

    # Lvl up attributes.
    st_points: int = field(default=0)
    sk_points: int = field(default=0)

    # Inventory attributes.
    inventory: Inventory = field(default=None)
    equip: dict = field(default=None)
    item_limits: dict = field(default=None)

    # Map attributes.
    map: np.array = field(default=None)
    map_labels: list = field(default=None)

    # Quests.
    quests_in_progress: list = field(factory=list)
    quests_completed: list = field(factory=list)

    # Skills attributes.
    skills: list[Skill] = field(factory=list)

    # Others.
    events: dict = field(default=None)
    time_played: timedelta = field(default=timedelta(seconds=0))

    def __attrs_post_init__(self):
        if len(self.name) > 12:
            self.name = self.name[:12]

        if self.last_place is None:
            self.last_place = Biome()

        if self.last_entry is None:
            self.last_entry = Entry()

        if self.inventory is None:
            self.inventory = Inventory()

        if self.item_limits is None:
            self.item_limits = {
                "little_red_potion": 5,
                "red_potion": 5,
                "giant_red_potion": 5,
                "antidote": 10
            }

        if self.map is None:
            self.map = np.zeros(shape=(MAP_X_LENGTH, MAP_Y_LENGTH, 4), dtype=np.uint8)
            self.map[:, :, 3] = np.ones(shape=(MAP_X_LENGTH, MAP_Y_LENGTH), dtype=np.uint8) * 255

        if self.map_labels is None:
            self.map_labels = [["UNEXPLORED" for _ in range(MAP_X_LENGTH)] for _ in range(MAP_Y_LENGTH)]

        if self.equip is None:
            self.equip = {BodyPart.HEAD: None,
                          BodyPart.CHEST: None,
                          BodyPart.RIGHT_HAND: None,
                          BodyPart.LEFT_HAND: None,
                          BodyPart.WAIST: None,
                          BodyPart.LEGS: None}

        else:
            # Make sure equip is a dictionary with the correct keys.
            valid_keys = set(BodyPart)
            self.equip = {key: self.equip.get(key) for key in valid_keys}

        if self.events is None:
            self.events = {
                "goblin_chief_crown_1": False,
                "goblin_chief_crown_2": False,
                "goblin_chief_crown_3": False,

                "marlin_quests_1": False,
                "marlin_quests_2": False,
                "marlin_quests_3": False,
                "marlin_quests_4": False,
                "caravan_date_arrive": None,
                "caravan_arrive": False,
                "marlin_quests_5": False,
                "marlin_quests_6": False,
                "antinas_permission": False,

                "dragon_win": False,
            }

    @property
    def attack(self) -> int:
        item_attack_sum = sum(item.attack for item in self.equip.values() if isinstance(item, Item))
        return int(self.b_attack + self.strength * self.attack_factor + item_attack_sum)

    @property
    def defense(self) -> int:
        item_defense_sum = sum(item.defense for item in self.equip.values() if isinstance(item, Item))
        return int(self.b_defense + self.resistance * self.defence_factor + item_defense_sum)

    @property
    def evasion(self) -> float:
        item_evasion_sum = sum(item.evasion for item in self.equip.values() if isinstance(item, Item))
        return self.b_evasion + self.agility * self.evasion_factor + item_evasion_sum

    @property
    def precision(self) -> float:
        item_precision_sum = sum(item.precision for item in self.equip.values() if isinstance(item, Item))
        return self.b_precision + self.agility * self.precision_factor + item_precision_sum

    @property
    def speed(self) -> float:
        return self.agility - self.current_weight * 0.1

    @property
    def hpmax(self) -> int:
        return int(self.b_hpmax + self.vitality * self.vitality_factor)

    @property
    def vital_energy_max(self) -> int:
        return int(self.b_vital_energy + self.vitality * self.vital_energy_factor)

    @property
    def exploration_radius(self):
        return self.vision + sum([item.vision for item in self.inventory.get_item_objects])

    @property
    def weight_carry(self):
        return self.strength * 2.5 + self.b_weight_carry

    @property
    def current_weight(self):
        return sum([self.inventory.get_item_object(item=item).weight * quantity
                    for item, quantity in self.inventory.items.items()])

    @property
    def move_available(self):
        return True if self.current_weight <= self.weight_carry else False

    @property
    def belt(self) -> Item | None:
        if self.equip[BodyPart.WAIST]:
            return self.equip[BodyPart.WAIST]
        return None

    # Current status methods.
    def has_vital_energy(self) -> bool:
        if hasattr(self, "vital_energy"):
            if self.vital_energy > 0:
                return True
        return False

    def is_alive(self) -> bool:
        return self.hp > 0

    def heal(self, amount: int) -> None:
        if self.hp + amount < self.hpmax:
            self.hp += amount
            return
        self.hp = self.hpmax

    def heal_poisoning(self, amount: int) -> None:
        for status in self.statuses:
            if status.status_type == StatusType.POISON:
                if status.stacks <= amount:
                    self.statuses.remove(status)
                    return
                status.stacks -= amount

    def recover_vital_energy(self, amount: int) -> None:
        self.vital_energy = min(self.vital_energy + amount, self.vital_energy_max)

    def use_vital_energy(self, amount: int) -> bool:
        if self.vital_energy >= amount:
            self.vital_energy -= amount
            return True
        return False

    def get_vital_energy(self) -> int:
        return self.vital_energy

    # Player lvl up attributes.
    def add_exp(self, amount: int) -> bool:
        self.exp += amount

        if self.exp >= self.expmax:
            self.lvl_up()
            return True
        else:
            return False

    def lvl_up(self, quantity: int = 1) -> None:
        self.level += quantity
        self.exp = 0
        self.expmax = 10 * self.level + self.level ** 2
        self.st_points += 3 * quantity

        self.b_hpmax += 2 * quantity
        self.b_attack += 0.4 * quantity
        self.b_defense += 0.20 * quantity
        self.b_precision += 0.005 * quantity
        self.b_evasion += 0.01 * quantity

    # Player place methods.
    def set_place(self, place: Biome | Entry) -> None:
        if type(self.place) == Entry:
            self.last_entry = self.place
        self.last_place = self.place

        if type(place) == Entry:
            self.outside = False
        else:
            self.x = place.x
            self.y = place.y
            self.outside = True
        self.place = place

    # Player inventory methods.
    def has(self, item: str, amount: int = None) -> bool:
        if amount is None:
            amount = 1
        return self.inventory.has(item=item, amount=amount)

    def has_slots(self) -> bool:
        if self.equip[BodyPart.WAIST] is not None:
            return self.equip[BodyPart.WAIST].has_slot()
        return False

    def has_slot_empty(self) -> bool:
        if self.equip[BodyPart.WAIST] is not None:
            return self.equip[BodyPart.WAIST].has_slot_empty()
        return False

    def get_gold(self) -> int:
        return self.inventory.get_gold()

    def get_item_quantity(self, item: Item) -> int:
        if item is None:
            return 0
        return self.inventory.get_item_quantity(item=item.id)

    def get_slots_quantity(self) -> int:
        return self.equip[BodyPart.WAIST].get_slot_quantity()

    def get_slot_item(self, slot: int) -> Item | None:
        if self.equip[BodyPart.WAIST] is not None:
            belt = self.equip[BodyPart.WAIST]
            return belt.get_slot_item(slot=slot)
        return None

    def get_slot_items(self) -> list[Item]:
        if self.belt is not None:
            return self.belt.get_slot_items()
        return []

    def get_first_slot_empty(self) -> int | None:
        if self.equip[BodyPart.WAIST] is not None:
            return self.equip[BodyPart.WAIST].get_first_slot_empty()

    def set_slot(self, slot: int, item: Item) -> bool:
        return self.equip[BodyPart.WAIST].set_slot(slot=slot, item=item)

    def add_item(self, item: Item, quantity: int = 1) -> None:
        if item.id in self.item_limits:
            if item.id not in self.inventory.items:
                if quantity >= self.item_limits[item.id]:
                    self.inventory.add_item(item=item, quantity=self.item_limits[item])
                    return
                self.inventory.add_item(item=item, quantity=quantity)
                return
            if self.inventory.items[item.id] + quantity >= self.item_limits[item.id]:
                self.inventory.items[item.id] = self.item_limits[item.id]
                return
            self.inventory.add_item(item=item, quantity=quantity)
            return
        self.inventory.add_item(item=item, quantity=quantity)
        self.update_quests(target=item.id, amount=quantity)

    def get_item(self, item: str) -> Item:
        return self.inventory.get_item_object(item=item)

    def get_equiped_item(self, item: str) -> Item | None:
        for equiped_item in self.get_equiped_items():
            if equiped_item.id == item:
                return equiped_item
        return None

    def get_equiped_items(self) -> list[Item]:
        items = [item for item in self.equip.values() if item is not None]
        if self.belt:
            items.extend([item for item in self.belt.get_slot_items() if item is not None])
        return items

    def equip_item(self, item: Item) -> None:
        if item.equippable and self.equip[item.body_part] is None:
            self.equip[item.body_part] = item
            return
        if self.has_slot_empty():
            self.set_slot(slot=self.get_first_slot_empty(), item=item)

    def unequip_item(self, item: Item) -> None:
        if item in self.equip.values() and item.equippable:
            self.equip[item.body_part] = None
        for i, slot in enumerate(self.get_slot_items()):
            if item.id == slot.id:
                self.belt.clear_slot(slot=i)

    def is_equiped(self, item: Item | str) -> bool:
        if isinstance(item, Item):
            if item in self.equip.values():
                return True
        if isinstance(item, str):
            if item in [item.id for item in self.get_equiped_items()]:
                return True
        return False

    # Map methods.
    def get_biome_label(self, x: int, y: int) -> str:
        return self.map_labels[y][x]

    # Quest methods.
    def add_quest(self, quest: Quest) -> None:
        self.quests_in_progress.append(quest)

    def get_quests(self, in_progress: bool = True, completed: bool = True) -> list[Quest]:
        quests = []
        if in_progress:
            quests.extend(self.quests_in_progress)
        if completed:
            quests.extend(self.quests_completed)
        return quests

    def remove_quest(self, quest: Quest) -> None:
        if quest.is_completed():
            self.quests_completed.append(quest)
            self.quests_completed.sort(key=lambda q: q.title)
            self.quests_in_progress.remove(quest)

    def update_quests(self, target: str, amount: int, deliver_item: str = None, deliver_amount: int = None) -> None:
        for quest in self.quests_in_progress:
            quest.update_progress(target=target,
                                  amount=amount,
                                  deliver_item=deliver_item,
                                  deliver_amount=deliver_amount)

    def refresh_quests(self) -> None:
        for quest in self.get_quests(completed=False):
            for objetive in filter(lambda obj: obj.status_type == ObjectiveType.COLLECT, quest.objectives):
                target = objetive.target
                quest.update_progress(target=target, amount=self.inventory.items.get(target, 0), carry=True)

    # Skill methods.
    def is_skill_available(self, skill: Skill) -> tuple[bool, int, str]:
        if self.vital_energy < skill.cost:
            return False, RequirementType.VITAL_ENERGY.value, f"{skill.cost}"
        return skill.check_requirements(caster=self)

    def add_skill(self, skill: Skill) -> None:
        self.skills.append(skill)

    def has_skill(self) -> bool:
        for skill in self.skills:
            if skill.id != "attack":
                return True
        return False

    # Buff methods.
    def has_buffs(self) -> bool:
        return bool(self.buffs)

    def add_buff(self, buff: Buff) -> None:
        self.buffs.append(copy.deepcopy(buff))

    def add_buff_applied(self, buff: Buff) -> None:
        self.buffs_applied.append(buff)

    def remove_buff(self, buff: Buff) -> None:
        self.buffs.remove(buff)

    def remove_buff_applied(self, buff: Buff) -> None:
        self.buffs_applied.remove(buff)

    def refresh_buffs(self) -> None:
        for buff in self.buffs:
            buff.apply(entitie=self)
            self.add_buff_applied(buff=buff)
            self.remove_buff(buff=buff)
        for buff in self.buffs_applied:
            buff.tick(entity=self)
            if not buff.is_active():
                buff.expire(entitie=self)
                self.remove_buff_applied(buff=buff)

    # Status methods.
    def is_poison(self) -> bool:
        return self.poison

    def is_freeze(self) -> bool:
        return self.freeze

    def is_burn(self) -> bool:
        return self.burn

    def is_stun(self) -> bool:
        return self.stun

    def is_bleed(self) -> bool:
        return self.bleed

    def is_paralyze(self) -> bool:
        return self.paralyze

    def set_stun(self, value: bool) -> None:
        self.stun = value

    def set_paralyze(self, value: bool) -> None:
        self.paralyze = value

    def refresh_hungry(self, hour: int, last_hour: int) -> None:
        if self.hungry > 0:
            self.hungry = max(0, self.hungry - (hour - last_hour))
            return
        self.hungry = 0

    def refresh_thirsty(self, hour: int, last_hour: int) -> None:
        if self.thirsty > 0:
            self.thirsty = max(0, self.thirsty - (hour - last_hour) // 2)
            return
        self.thirsty = 0

    def refresh_vital_energy(self, hour: int, last_hour: int) -> None:
        self.recover_vital_energy(amount=self.vitality // 3 * ((hour - last_hour) // 12))

    def refresh_temperature(self) -> None:
        temperature = self.place.temperature
        for item in self.equip.values():
            if item is None:
                continue
            temperature += item.warmness
        self.temperature = temperature

    def refresh_temperature_status(self) -> None:
        self.refresh_temperature()
        if self.temperature > 45:
            self.add_status(status=Status.gen_freeze(duration=2, stacks=2, max_stacks=1, source="biome"))
        if 40 <= self.temperature <= 45:
            self.add_status(status=Status.gen_burn(duration=2, stacks=1, max_stacks=1, source="biome"))
        if 25 <= self.temperature <= 30:
            self.add_status(status=Status.gen_freeze(duration=2, stacks=1, max_stacks=1, source="biome"))
        if self.temperature <= 25:
            self.add_status(status=Status.gen_freeze(duration=2, stacks=2, max_stacks=1, source="biome"))

    def refresh_status(self, onbattle: bool = False) -> None:
        self.set_stun(value=False)
        self.set_paralyze(value=False)
        self.discard_save_statuses()
        for status in self.statuses:
            if status.is_damaging():
                self.hp -= status.stacks
            if status.is_sttuner():
                self.set_stun(value=True)
            if status.is_paralyzer():
                self.set_paralyze(value=True)
            status.tick(entity=self)
            if status.duration <= 0:
                self.add_save_status(status=status)
                self.discard_status(status=status)

        if not onbattle:
            if self.hungry < 10:
                self.hp -= 1

            if self.thirsty < 10:
                self.hp -= 1

    def add_hungry(self, amount: int) -> None:
        if self.hungry + amount > 100:
            self.hungry = 100
            return
        self.hungry += amount

    def add_thirsty(self, amount: int) -> None:
        if self.thirsty + amount > 100:
            self.thirsty = 100
            return
        self.thirsty += amount

    def add_status(self, status: Status) -> None:
        active_status = self.get_status(status_type=status.status_type)
        if active_status is not None:
            active_status.apply_stack(other=status)
            return
        self.statuses.append(copy.deepcopy(status))

    def add_save_status(self, status: Status) -> None:
        self.statuses_save.append(status)

    def discard_status(self, status: Status) -> None:
        self.statuses.remove(status)

    def discard_save_statuses(self) -> None:
        self.statuses_save.clear()

    def get_status(self, status_type: Enum) -> Status | None:
        for status in self.statuses:
            if status_type == status.status_type:
                return status

    # Fighting methods.
    def get_standar_attack(self) -> Skill:
        for skill in self.skills:
            if skill.id == "attack":
                return skill

    def attack_to(self, target) -> tuple[bool, bool, int, bool, list]:
        skill = self.get_standar_attack()
        return skill.action(caster=self, target=target)
        
    def take_damage(self, damage: int) -> int:
        efective_dmg = max(0, damage - self.defense)
        self.hp = max(0, self.hp - efective_dmg)
        return efective_dmg

    # Other methods.
    def refresh_time_played(self, time_close: timedelta | datetime, time_init: timedelta | datetime) -> None:
        self.time_played = time_close - time_init + self.time_played

    # Move and actions methods.
    def get_available_actions(self, onbattle: bool = False) -> tuple[list, list]:
        actions = []
        action_labels = []
        if not onbattle:
            actions.append(Actions.SAVE_AND_QUIT)
            action_labels.append("SAVE AND QUIT")

        if self.is_stun():
            actions.append(Actions.WAIT)
            action_labels.append("WAIT")
            return actions, action_labels

        if self.is_paralyze() and not self.is_stun():
            actions.append(Actions.WAIT)
            action_labels.append("WAIT")
            if self.has_skill():
                actions.append(Actions.SKILL)
                action_labels.append("SKILL")
            return actions, action_labels

        if onbattle:
            actions.append(Actions.ESCAPE)
            action_labels.append("ESCAPE")
            actions.append(Actions.HIT_ATTACK)
            action_labels.append("ATTACK")

        if self.has_skill():
            actions.append(Actions.SKILL)
            action_labels.append("SKILL")
        if self.has_slots():
            for slot_number in range(self.get_slots_quantity()):
                actions.append(Actions.USE_ITEM)
                item = self.get_slot_item(slot=slot_number)
                item_name = item.name.upper() if item is not None else "None"
                quantity = self.get_item_quantity(item=item)
                action_labels.append(f"{item_name} [{quantity}]")
        return actions, action_labels
