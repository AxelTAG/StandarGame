# Imports.
# Local imports.
from .use import use
from .. import displays
from .. import enums
from ..map import Map
from ..mob import Mob
from ..player import Player
from ..status import Status
from ..utils import reset_map, underscores

# External imports.
import random
from attrs import field, define

STANDARD_VICTORY_MSG = "Victory! You defeated all enemies."
STANDARD_DEFEAT_MSG = "The enemy has defeat you..."
STANDARD_PARTY_DEFEAT_MSG = "Defeat... Your party has fallen."
STANDARD_FIRST_MSG = "Defeat the enemy!"
STANDARD_ESCAPE_MSG = "You have escaped."
STANDARD_NOT_ESCAPE_MSG = "You have not escaped."
STANDARD_NOT_ENOUGH_VT_MSG = "You have not enough vital energy."
STANDARD_NOT_ENOUGH_LEVEL_MSG = "You don't have the required level to use this skill."
STANDARD_NOT_EQUIPED_MSG = "You don't have the required equipment to use this skill."
STANDARD_NOT_ITEM_MSG = "You don't have the required item to use this skill."
STANDARD_NOT_STATS_MSG = "You don't have the required stats to use this skill."


def get_number(floor_n: int = 0, ceil_n: int = 10) -> int | None:
    while True:
        try:
            number = int(input(displays.INPUT_LABEL_BATTLE))
            if floor_n <= number <= ceil_n:
                return number
        except ValueError:  # Bucle will reset if input is not an intenger.
            pass


@define
class Battle:
    # Entities attributes.
    players: list[Player] | Player
    enemies: list[Mob] | Mob
    mapgame: Map
    turn: int = field(default=1)

    # Escape attributes.
    escape: bool = field(default=False)
    escape_chance: float = field(default=None)

    # Display attributes.
    screen: list = field(default=None)

    # Default messages atrributes.
    msg_victory: str = field(default=None)
    msg_defeat: str = field(default=None)
    msg_escape: str = field(default=None)
    msg_not_escape: str = field(default=None)
    msg_lvl_up: str = field(default=None)

    # Map game settings atrributes.
    pace_factor: float = field(default=0.2)

    # Result battle attributes.
    win: bool = field(init=False)

    def __attrs_post_init__(self) -> None:
        # Escape attributes.
        if self.escape_chance is None:
            self.escape_chance = max([enemy.escape_chance for enemy in self.enemies])

        # Default messages atrributes.
        if self.screen is None:
            self.screen = [STANDARD_FIRST_MSG]
        if self.msg_victory is None:
            self.msg_victory = STANDARD_VICTORY_MSG
        if self.msg_defeat is None:
            if len(self.enemies) == 1:
                self.msg_defeat = STANDARD_DEFEAT_MSG
            if len(self.enemies) > 1:
                self.msg_defeat = STANDARD_PARTY_DEFEAT_MSG
        if self.msg_escape is None:
            self.msg_escape = STANDARD_ESCAPE_MSG
        if self.msg_not_escape is None:
            self.msg_not_escape = STANDARD_NOT_ESCAPE_MSG
        if self.msg_lvl_up is None:
            self.msg_lvl_up = displays.PLAYER_LVL_UP_MSG

        # Result battle attributes.
        self.win = False

    def get_turn_order(self) -> list[Player | Mob]:
        entities = [entitie for entitie in self.players + self.enemies if entitie.is_alive()]
        return sorted(entities, key=lambda entitie: entitie.speed, reverse=True)

    def select_target_enemy(self) -> Mob:
        alive_enemies = [enemy for enemy in self.enemies if enemy.is_alive()]
        if len(alive_enemies) == 1:
            return alive_enemies[0]
        displays.disp_enemies(enemies=alive_enemies, display=True)
        selection = get_number(floor_n=1, ceil_n=len(alive_enemies)) - 1
        return alive_enemies[selection]

    def player_action(self, player: Player, enemies: list[Mob]) -> bool:
        # Action selection and display.
        actions, _ = player.get_available_actions(onbattle=True)
        choice = get_number(floor_n=0, ceil_n=len(actions) - 1)
        action_type = actions[choice]

        # Action execution.
        if action_type == enums.Actions.ESCAPE:
            if self.escape_chance >= random.randint(a=0, b=99):
                self.screen.append(self.msg_escape)
                self.escape = True
                return True
            self.screen.append(self.msg_not_escape)
            return True

        elif action_type == enums.Actions.WAIT:
            self.screen.append(f"You have wait.")
            return True

        elif action_type == enums.Actions.HIT_ATTACK:
            target = self.select_target_enemy()
            fail, _, damage, critical, _ = player.attack_to(target=target)
            if fail:
                self.screen.append(f"{player.name} has failed the attack.")
                return True
            self.screen.append(f"{player.name} has dealt {damage} to {target.name}.")
            if critical:
                self.screen[-1] += " Critical hit!"
            return True

        elif action_type == enums.Actions.SKILL:
            displays.disp_skill_selection(entitie=player, prefix=" ")
            number = get_number(floor_n=1, ceil_n=len(player.skills) - 1)
            if 0 <= number < len(player.skills):
                skill = player.skills[number]
                target = self.select_target_enemy()
                avaible, requirement, cause = player.is_skill_available(skill=skill)
                if avaible:
                    fail, _, damage, critical, effects = skill.action(caster=player, target=target, onbattle=True)
                    if fail:
                        self.screen.append(f"{player.name} has failed the skill {skill.name}.")
                    if critical:
                        self.screen[-1] += " Critical hit!"
                    if effects:
                        effect_names = [effect.name for effect in effects]
                        self.screen.append(
                            f"{player.name}’s skill caused the following effects: {', '.join(effect_names)}.")
                    if not fail:
                        self.screen.append(f"{player.name} has casted {skill.name} and has dealt {damage}.")
                    return True
                if requirement == enums.RequirementType.VITAL_ENERGY.value:
                    self.display(screen=STANDARD_NOT_ENOUGH_VT_MSG,
                                 players=self.players,
                                 enemies=self.enemies,
                                 clear=False)
                    return False
                if requirement == enums.RequirementType.LVL.value:
                    self.display(screen=STANDARD_NOT_ENOUGH_LEVEL_MSG,
                                 players=self.players,
                                 enemies=self.enemies,
                                 clear=False)
                    return False
                if requirement == enums.RequirementType.EQUIP.value:
                    self.display(screen=f"{STANDARD_NOT_EQUIPED_MSG}\n({cause})",
                                 players=self.players,
                                 enemies=self.enemies,
                                 clear=False)
                    return False
                if requirement == enums.RequirementType.ITEM.value:
                    self.display(screen=STANDARD_NOT_ITEM_MSG,
                                 players=self.players,
                                 enemies=self.enemies,
                                 clear=False)
                    return False
                if requirement == enums.RequirementType.STATS.value:
                    self.display(screen=STANDARD_NOT_STATS_MSG,
                                 players=self.players,
                                 enemies=self.enemies,
                                 clear=False)
                    return False

        elif action_type == enums.Actions.USE_ITEM:
            slot_number = choice - (len(actions) - player.get_slots_quantity())
            msg, succes = use(player=player, item=player.get_slot_item(slot=slot_number))
            if succes:
                self.screen.append(msg)
                return succes
            self.display(screen=msg,
                         players=self.players,
                         enemies=self.enemies,
                         clear=False)
            return succes

    def enemy_action(self, enemy: Mob, players: list[Player]) -> None:
        if enemy.is_stun():
            self.screen.append(f"{enemy.name} was stunned and cannot attack.")
            return
        if enemy.is_paralyze():
            self.screen.append(f"{enemy.name} was paralyzed and cannot attack.")
            return

        target = random.choice([player for player in players if player.is_alive()])
        fail, _, damage, critical, effects = enemy.attack_to(target=target, onbattle=True)
        if fail:
            self.screen.append(f"{enemy.name} has failed the attack.")
            return
        self.screen.append(f"{enemy.name} has dealt {damage} to {target.name}.")
        if critical:
            self.screen[-1] += " Critical hit!"
        if effects:
            effect_names = [effect.name for effect in effects]
            self.screen.append(f"{enemy.name}’s attack caused the following effects: {', '.join(effect_names)}.")
        return

    def is_victory(self) -> bool:
        return all(not enemy.is_alive() for enemy in self.enemies)

    def is_defeat(self) -> bool:
        return all(not player.is_alive() for player in self.players)

    def apply_statuses(self):
        """Applies effects of all active statuses."""
        for entity in self.players + self.enemies:
            if not entity.is_alive():
                continue
            entity.refresh_status(onbattle=True)

    def reward_objects(self) -> None:
        rewards = []
        for enemy in self.enemies:
            for item in enemy.drop_items():
                rewards.extend([item] * enemy.items[item])
                item_name = underscores(text=item, delete=True).title()
                self.screen.append(f"{enemy.name} has dropped {enemy.items[item]} {item_name}.")
                print()
        random.shuffle(rewards)
        n = len(rewards) // len(self.players)
        for i, player in enumerate(self.players):
            player_reward = rewards[i * n: (i + 1) * n]
            for item in player_reward:
                item_object = self.mapgame.get_item_object(item_id=item)
                player.add_item(item=item_object, quantity=1)

    def reward_expirience(self) -> None:
        expirience = 0
        for enemy in self.enemies:
            expirience += enemy.get_experience()
        for player in self.players:
            if player.add_exp(amount=expirience // len(self.players)):
                self.screen.append(self.msg_lvl_up)

    def display(self, screen: str, players: list[Player] = None, enemies: list[Mob] = None, clear: bool = True) -> None:
        displays.disp_battle(players=players,
                             enemies=enemies,
                             screen=screen)
        if clear:
            self.clear_screen()

    def update_quest(self) -> None:
        for player in self.players:
            for enemy in self.enemies:
                player.update_quests(target=enemy.id_key, amount=1)

    def remove_mobs(self) -> None:
        for enemy in self.enemies:
            self.players[0].place.remove_mob_respawned(mob=enemy)

    def run(self):
        while not self.is_victory() and not self.is_defeat():
            self.display(screen=self.compile_strings(strings=self.screen),
                         players=self.players,
                         enemies=self.enemies)

            for entity in self.get_turn_order():
                if not entity.is_alive():
                    continue

                if entity in self.players:
                    while not self.player_action(player=entity, enemies=self.enemies):
                        pass
                if entity in self.enemies:
                    self.enemy_action(enemy=entity, players=self.players)
                if self.is_victory() or self.is_defeat():
                    break

            if self.escape:
                break
            self.apply_statuses()
            self.turn += 1
            self.pause()

        if self.is_victory():
            self.screen.append(self.msg_victory)
            self.reward_objects()
            self.reward_expirience()
            self.update_quest()
            self.remove_mobs()
            self.win = True
        if self.is_defeat():
            self.screen.append(self.msg_defeat)
        if self.escape:
            pass
        self.display(players=self.players, enemies=self.enemies, screen=self.compile_strings(self.screen))
        self.mapgame.add_hours(hours_to_add=int(self.turn * self.pace_factor))
        self.pause()

        return self.win

    def clear_screen(self, display: bool = False) -> None:
        self.screen = []
        if display:
            self.display(screen=self.compile_strings(strings=self.screen))

    @staticmethod
    def pause() -> None:
        input(displays.PAUSE_LABEL)

    @staticmethod
    def compile_strings(strings: list[str]) -> str:
        return "\n ".join(strings)

    @staticmethod
    def process_attack(caster: Player | Mob, target: Player | Mob) -> int:
        pass


def battle(players: list[Player], enemies: list[Mob], mapgame: Map, **kwargs) -> int:
    fight = Battle(players=players, enemies=enemies, mapgame=mapgame, **kwargs)
    return fight.run()
