# Imports.
# Internal imports.
import displays
from biome import Biome, Entry
from enums import EntryType, NpcTypes, PlayerStatus, TimeOfDay
from item import Item
from map import Map
from mob import Mob
from npc import Npc
from player import Player
from utils import reset_map, text_ljust, underscores
from world import ITEMS

# External imports.
import math
import os
import random

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


# ----------------------------------------------------------------------------------------------------
# Utiliy functions.
def get_item(item_name: str) -> Item | bool:
    if item_name in ITEMS.keys():
        return ITEMS[item_name]
    else:
        return False


# ----------------------------------------------------------------------------------------------------

def attack(player: Player,
           map_game: Map,
           mob: Mob) -> tuple[bool, bool, bool]:
    play, menu, win = battle(player=player,
                             map_game=map_game,
                             enemy=mob,
                             pace_factor=.05)
    return play, menu, win


# Battle action.
def battle(player: Player,
           map_game: Map,
           enemy: Mob,
           pace_factor: float = 0.025) -> tuple[bool, bool, bool]:
    screen = "Defeat the enemy!"
    play = True
    menu = False
    win = False
    fight = True
    hours_to_add = 0

    while fight:
        displays.disp_battle(player=player,
                             enemy=enemy,
                             text=screen)
        choice_action = input(" # ")  # User choice action.
        object_used = True
        screen = "Nothing done."  # Clearing text output screen.
        hours_to_add += player.place.get_pace(month=map_game.current_month) * pace_factor

        # Actions.
        if choice_action == "0":  # Escape option.
            escape = random.choices([True, False],
                                    weights=[enemy.escape_chance, 100 - enemy.escape_chance],
                                    k=1)[0]
            if escape:
                screen = "You have escaped."
                displays.disp_battle(player=player,
                                     enemy=enemy,
                                     text=screen)
                input(" > ")
                return play, menu, win
            else:
                screen = "You have not escaped."

        elif choice_action == "1":  # Attack option.
            if player.precision * (1 - enemy.evasion) > random.random():
                USER_DMG = max(int(int(player.attack) - int(enemy.defense)), 0)
                enemy.hp -= USER_DMG
                screen = f" {player.name} dealt {USER_DMG} damage to the {enemy.name}."
            else:
                screen = f" {player.name} fail the attack."

        elif choice_action in ["2", "3"]:  # Use object action.
            if choice_action == "2":
                screen, object_used = use(player, map_game=map_game, item=player.slot1)
            if choice_action == "3":
                screen, object_used = use(player, map_game=map_game, item=player.slot2)

        # Enemy attack.
        if enemy.escape_mob_probability > random.random():
            screen += f"\n {enemy.name} has escaped."
            displays.disp_battle(player=player,
                                 enemy=enemy,
                                 text=screen)
            input(" > ")
            return play, menu, win

        if enemy.hp > 0 and choice_action in ["0", "1", "2", "3"]:
            if enemy.precision * (1 - player.evasion) > random.random() and object_used:
                ENEMY_ATK = [[enemy.attack, enemy.attack * enemy.critical_coeficient],
                             [100 - enemy.critical_chance, enemy.critical_chance]]
                ENEMY_DMG = max(int(int(random.choices(ENEMY_ATK[0], ENEMY_ATK[1], k=1)[0]) - int(player.defense)), 0)
                player.hp -= ENEMY_DMG
                screen += "\n " + enemy.name + " dealt " + str(ENEMY_DMG) + " damage to " + player.name + "."

                if enemy.poison > 0 and enemy.poison_chance > random.random() and player.poison == 0:
                    player.poison = enemy.poison
                    screen += "\n " + enemy.name + " has poisoned you."
            else:
                screen += "\n " + enemy.name + " fail the attack."
        input(" > ")

        # Logic of fight status or result.
        # Lose.
        if player.hp <= 0:
            screen += "\n " + enemy.name + " defeated " + player.name + "..."
            displays.disp_battle(player=player, enemy=enemy, text=screen)
            input(" > ")

            # Setting reinit.
            play = False
            menu = True
            win = False
            player.hp = int(player.hpmax)
            player.set_place(place=map_game.map_settings[(player.x_cp, player.y_cp)])
            player.status = 0
            player.poison = 0
            player.hungry = 48
            player.thirsty = 48
            player.exp = 0
            reset_map(ms=map_game.map_settings, keys=[(2, 1), (6, 2)])

            print(" LOST DREAM")
            input(" > ")
            return play, menu, win

        # Win.
        if enemy.hp <= 0:
            win = True
            screen += f"\nYou defeated the {enemy.name}!"
            map_game.add_hours(hours_to_add=int(hours_to_add))

            # Drop items logic and experience gain.
            if enemy.items:
                for item in enemy.drop_items():
                    item_name = underscores(text=item, delete=True)
                    player.add_item(item=item, quantity=enemy.items[item])
                    screen += f"\n You've found {enemy.items[item]} {item_name}."

            screen += f"\n You have gained {enemy.experience} experience."

            if player.add_exp(enemy.experience):
                screen += " You have lvl up. ASSIGN Strength/Agility/Vitality. You can assign 3 points."

            # Remove of mob at biome.
            player.place.remove_mob_respawned(mob=enemy)

            displays.disp_battle(player=player,
                                 enemy=enemy,
                                 text=screen)
            input(" > ")

            return play, menu, win


# Buy action.
def buy(player: Player, item: str, quantity: int, price: int) -> tuple[str, bool]:
    """
    Attempts to buy a specified quantity of an item for a player if they have enough gold.

    The function checks if the player has sufficient gold to purchase the desired quantity of the item at the given
    price.
    If successful, the item is added to the player's inventory, and the gold is deducted from their balance.
    If the player doesn't have enough gold, the purchase is rejected.

    :param player: The player making the purchase. It must be an instance of the `Player` class.
    :type player: Player
    :param item: The name of the item to purchase.
    :type item: str
    :param quantity: The quantity of the item to purchase.
    :type quantity: int
    :param price: The price per unit of the item.
    :type price: int

    :return: A message indicating the result of the transaction and a boolean that is `True` if the purchase is
    successful, otherwise `False`.
    :rtype: tuple[str, bool]
    """
    item_name = item.replace('_', ' ').title()
    if player.inventory.gold >= price * quantity:
        try:
            player.add_item(item=item, quantity=quantity)

        except KeyError:
            player.inventory.items[item] = 0
            player.add_item(item=item, quantity=quantity)
        player.inventory.gold -= price * quantity

        return f"You buy {quantity} {item_name}.", True

    else:
        return "You don't have enough gold.", False


# Check action.
def check(player: Player = None, item: str = None, inventory: bool = False) -> str:
    if player is None:
        return "What do you want to check? CHECK ITEM for items at places or CHECK INV ITEM for items in the inventory."

    if not item or item is None:
        return "What do you want to check? CHECK ITEM for items at places or CHECK INV ITEM for items in the inventory."

    if item in ITEMS.keys():
        if inventory:
            if item in player.inventory.items.keys():
                return ITEMS[item].description

        if item in player.place.get_items():
            return ITEMS[item].description
    return f"There is no {item.title()} here."


def craft(player: Player, item: str, quantity: int) -> tuple[str, bool]:
    if item not in ITEMS:
        return "This item cannot be craft.", False

    items = player.inventory.items
    item_object = ITEMS[item]
    item_name = item_object.name
    for mat, mat_amount in item_object.crafting_materials.items():
        material_name = mat.replace("_", " ").title()
        mat_amount_total = mat_amount * quantity
        if mat not in items:
            answer = f"You haven't {material_name} to craft {item_name}. You need {mat_amount_total} {material_name}."
            return answer, False
        if items[mat] < mat_amount * quantity:
            answser = (f"You haven't enough {material_name} to craft {item_name}."
                       f" You need {mat_amount_total} {material_name}.")
            return answser, False

    for mat, mat_amount in item_object.crafting_materials.items():
        player.inventory.discard_item(item=mat, quantity=mat_amount * quantity)

    player.add_item(item=item, quantity=quantity)

    return f"You crafted {quantity} {item_object.name}.", True


# Draw map action.
def draw_map(player: Player, map_game: Map, pace_factor: float = 0.5, exploration_radius: float = None) -> str:
    if not player.place.draw_map:
        return "You can't draw map here. You can't explore for it."

    if exploration_radius is None:
        exploration_radius = player.exploration_radius

    player.map[player.y][player.x] = map_game.map_settings[(player.x, player.y)].get_color(month=map_game.current_month)

    # Helper function to map specific coordinates.
    def map_tile(x: int, y: int):
        if 0 <= x < map_game.x_len and 0 <= y < map_game.y_len:
            player.map[y][x] = map_game.map_settings[(x, y)].get_color(month=map_game.current_month)

    # Map the boxes within the circular radius.
    for i in range(max(0, player.x - int(exploration_radius)),
                   min(map_game.x_len, player.x + int(exploration_radius) + 1)):
        for j in range(max(0, player.y - int(exploration_radius)),
                       min(map_game.y_len, player.y + int(exploration_radius) + 1)):
            # Checks if the cell is inside de circunference.
            if math.sqrt((player.x - i) ** 2 + (player.y - j) ** 2) <= exploration_radius:
                map_tile(i, j)

    # Add time based on venue tempo and pace factor.
    hours_to_add = int(player.place.get_pace(month=map_game.current_month) * pace_factor)
    map_game.add_hours(hours_to_add=hours_to_add)

    return "You have explored the area and mapped it out."


def drink(player: Player, item: str) -> str:
    item_name = item.replace("_", " ").title()
    item_object = get_item(item_name=item)

    if not item_object:
        return f"You don't have {item_name}."

    if not player.has(item=item, amount=1):
        return f"You don't have {item_object.name}."

    if not item_object.edible:
        return f"{item_object.name} is not edible."

    player.add_hungry(amount=item_object.hungry_refill)
    player.add_thirsty(amount=item_object.thirsty_refill)
    player.inventory.discard_item(item=item, quantity=1)
    return f"You have drunk {item_object.name}."


# Drop action.
def drop(player: Player, item: str, quantity: int = 1) -> str:
    item_name = item.replace("_", " ")
    item_object = get_item(item_name=item)

    if item is None:
        return "Cannot drop None."

    if not item_object:
        return f"You don't have {item_name}."

    if not item_object.droppable:
        return f"You can't drop {item_object.name}."

    if player.inventory.drop_item(item=item, quantity=quantity):
        player.place.add_item(item)
        return f"You drop {quantity} {item_name.title()}."
    return f"You don't have {quantity} {item_name}."


def eat(player: Player, item: str) -> str:
    item_name = item.replace("_", " ").title()
    item_object = get_item(item_name=item)

    if item is None:
        return f"Cannot eat None."

    if not item_object:
        return f"You don't have {item_name}."

    if not player.has(item=item, amount=1):
        return f"You don't have {item_object.name}."

    if not item_object.edible:
        return f"{item_object.name} is not edible."

    player.add_hungry(amount=item_object.hungry_refill)
    player.add_thirsty(amount=item_object.thirsty_refill)
    player.inventory.discard_item(item=item, quantity=1)
    return f"You have eaten {item_object.name}."


# Enter action.
def enter(player: Player, entrie: str, mapgame: Map) -> tuple[str, bool]:
    if not player.place.entries:
        return "There aren't entries here.", True

    if entrie is None:
        return "You need to specify the name more clearly.", True

    objects = [*player.inventory.items.keys()] + [*player.events.keys()]
    entry_name = entrie.replace("_", " ").title()

    if entrie not in player.place.entries.keys():
        return f"There is not a {entry_name} here.", True

    entrie_object = player.place.entries[entrie]
    if type(entrie_object) == Entry and not entrie_object.hide["visibility"]:
        return f"There is not a {entry_name} here.", True

    if all(req in objects for req in entrie_object.get_req(month=mapgame.current_month)):
        if type(entrie_object) == Entry:
            player.outside = False
        if type(entrie_object) == Biome:
            player.outside = True
        entrie_name = entrie_object.get_name(month=mapgame.current_month)
        player.set_place(entrie_object)
        return f"You have enter to the {entrie_name}.", False

    requirements = " ".join(entrie_object.get_req(mapgame=mapgame)).split("_")
    requirements = " ".join(requirements).title()
    return "You need " + requirements + " to enter.", True


# Equip action.
def equip(player: Player, item: str) -> str:
    item_name = item.replace('_', ' ').title()
    item_object = get_item(item_name=item)

    if not item_object:
        return f"You don't have {item_name}."

    if item not in player.inventory.items.keys():
        return f"You don't have {item_object.name}."

    if not item_object.equippable:
        return f"You can't equip {item_object.name}."

    if player.equip[item_object.body_part] is not None:
        return f"You already have an item equipped. UNEQUIP {item_object.body_part.name}."

    player.equip[item_object.body_part] = item_object
    player.inventory.drop_item(item=item, quantity=1)
    return f"You have equip {item_object.name}."


# Exit action.
def exit_entry(player: Player, map_game: Map) -> tuple[str, bool]:
    if player.outside:
        return "You are outside.", True

    if player.place.leave_entry is None:
        place = player.last_place
    else:
        place = player.place.leave_entry

    player.set_place(place)

    return f"You left the {player.last_place.get_name(month=map_game.current_month)}.", False


# Explore action.
def explore(player: Player, map_game: Map, pace_factor: float = 0.5) -> str:
    if player.place.entries is None:
        map_game.add_hours(hours_to_add=int(player.place.get_pace(month=map_game.current_month) * pace_factor))
        return "You explore the zone but you found nothing."

    if isinstance(player.place, Entry):
        if player.place.entry_type not in [EntryType.CAVE]:
            return "You can't explore here."

    for key_entrie, entrie in player.place.entries.items():
        if type(entrie) == Biome:
            continue
        if entrie.hide is None:
            continue
        if entrie.hide["visibility"]:
            continue
        else:
            if entrie.hide["finding_chance"] >= random.random():
                entrie.hide["visibility"] = True
                map_game.add_hours(hours_to_add=int(player.place.get_pace(month=map_game.current_month) * pace_factor))
                return f"You have found a {entrie.name}."
            map_game.add_hours(hours_to_add=int(player.place.get_pace(month=map_game.current_month) * pace_factor))
            return "You explore the zone but you found nothing."
    map_game.add_hours(hours_to_add=int(player.place.get_pace(month=map_game.current_month) * pace_factor))
    return f"You explore the zone but you found nothing."


def fish(player: Player, map_game: Map, pace_factor: float = 0.3) -> str:
    if not any([item.fishing for item in player.inventory.get_item_objects]):
        return "You need a fishingpole to fish."

    if not player.place.get_water(month=map_game.current_month):
        return "You cannot fish here."

    probability = 0.95 if player.place.get_name(month=map_game.current_month) != "SEA" else 0.99
    if random.random() > probability:
        fish_caught = random.choices(player.place.get_fishs(month=map_game.current_month), k=1)[0]
        fish_caught_name = fish_caught.replace("_", " ").title()
        player.add_item(item=fish_caught, quantity=1)
        map_game.add_hours(hours_to_add=int(player.place.get_pace(month=map_game.current_month) * pace_factor))
        return f"You have caught a {fish_caught_name}."

    else:
        map_game.add_hours(hours_to_add=int(player.place.get_pace(month=map_game.current_month) * pace_factor))
        return "You haven't caught anything."


# Heal action.
def heal(player: Player, amount: int) -> tuple[str, int]:
    player.heal(amount=amount)
    return player.name + "'s HP refilled to " + str(player.hp) + "!", player.hp


# Land.
def land(player: Player, map_game: Map, pace_factor: float = 0.2) -> str:
    x, y = player.x, player.y

    if player.status == PlayerStatus.SURF.value and map_game.map_labels[y][x] not in ["sea", "river"]:
        player.status = PlayerStatus.WALK.value

        map_game.map_settings[(x, y)].items.append("boat")
        if not map_game.map_settings[(x, y)].description.items().count("boat"):
            for k, v in map_game.map_settings[(x, y)].description.items():
                map_game.map_settings[(x, y)].description[k] += " Anchored boat gently resting by the shore."

        map_game.add_hours(hours_to_add=int(player.place.get_pace(month=map_game.current_month) * pace_factor))
        return "You have land."

    else:
        if player.status == PlayerStatus.SURF.value:
            return "You can't land here."

        else:
            return "You aren't in a boat."


def listen(player: Player, map_game: Map, entitie: str) -> str:
    entitie_name = entitie.replace("_", " ").title()
    if entitie_name == "":
        return "You need to specify a name/thing."

    if entitie in player.place.get_items():
        if ITEMS[entitie].tracks is None:
            return f"You listen nothing special from {entitie_name}."

        track = ITEMS[entitie].tracks[map_game.current_week_day]
        if track is not None:
            pygame.mixer.music.load(track)
            pygame.mixer.music.play(0)
        return f"You are listening to {entitie_name}."

    if entitie in player.place.get_npc():
        if map_game.npcs[entitie].tracks is None:
            return f"You listen nothing special from {entitie_name}."

        track = map_game.npcs[entitie].tracks[map_game.current_week_day]
        if track is not None:
            pygame.mixer.music.load(track)
            pygame.mixer.music.play(0)
            return f"You are listening to {entitie_name}."
        return f"You listen nothing special from {entitie_name}."

    return f"There is no {entitie_name} here."


# Move function.
def move(player: Player,
         map_game: Map,
         mv: str,
         pace_factor: float = 1) -> tuple[str, bool]:
    x, y = player.x, player.y
    map_height, map_width = map_game.x_len, map_game.y_len
    tl_map, ms = map_game.map_labels, map_game.map_settings
    inventory = player.inventory.items
    events = [event for event in player.events.keys() if event == True]

    # Move North.
    if (y > 0 and all(req in [*inventory.keys()] + events for req in ms[(x, y - 1)].get_req(month=map_game.current_month)) and player.status
            in ms[(x, y - 1)].get_status(month=map_game.current_month) and mv == "1"):
        if (tl_map[y - 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (
                tl_map[y - 1][x] != "town" and tl_map[y][x] != "town") or (
                tl_map[y][x] == "town" and tl_map[y - 1][x] in ["town", "gates"]):
            player.x, player.y = x, y - 1
            player.set_place(place=map_game.map_settings[(player.x, player.y)])
            map_game.add_hours(hours_to_add=int(player.place.get_pace(month=map_game.current_month) * pace_factor))
            return "You moved North.", False

    # Move East.
    if (x < map_height and all(
            req in [*inventory.keys()] + events for req in ms[(x + 1, y)].get_req(month=map_game.current_month)) and player.status
            in ms[(x + 1, y)].get_status(month=map_game.current_month) and mv == "2"):
        if (tl_map[y][x + 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (
                tl_map[y][x + 1] != "town" and tl_map[y][x] != "town") or (
                tl_map[y][x] == "town" and tl_map[y][x + 1] in ["town", "gates"]):
            player.x, player.y = x + 1, y
            player.set_place(place=map_game.map_settings[(player.x, player.y)])
            map_game.add_hours(hours_to_add=int(player.place.get_pace(month=map_game.current_month) * pace_factor))
            return "You moved East.", False

    # Move South.
    if (y < map_width and all(
            req in [*inventory.keys()] + events for req in ms[(x, y + 1)].get_req(month=map_game.current_month)) and player.status
            in ms[(x, y + 1)].get_status(month=map_game.current_month) and mv == "3"):
        if (tl_map[y + 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (
                tl_map[y + 1][x] != "town" and tl_map[y][x] != "town") or (
                tl_map[y][x] == "town" and tl_map[y + 1][x] in ["town", "gates"]):
            player.x, player.y = x, y + 1
            player.set_place(place=map_game.map_settings[(player.x, player.y)])
            map_game.add_hours(hours_to_add=int(player.place.get_pace(month=map_game.current_month) * pace_factor))
            return "You moved South.", False

    # Move West.
    if (x > 0 and all(req in [*inventory.keys()] + events for req in ms[(x - 1, y)].get_req(month=map_game.current_month)) and player.status
            in ms[(x - 1, y)].get_status(month=map_game.current_month) and mv == "4"):
        if (tl_map[y][x - 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (
                tl_map[y][x - 1] != "town" and tl_map[y][x] != "town") or (
                tl_map[y][x] == "town" and tl_map[y][x - 1] in ["town", "gates"]):
            player.x, player.y = x - 1, y
            player.set_place(place=map_game.map_settings[(player.x, player.y)])
            map_game.add_hours(hours_to_add=int(player.place.get_pace(month=map_game.current_month) * pace_factor))
            return "You moved West.", False

    return "You can't move there.", True


# Look around action.
def look_around(player: Player, map_game: Map, pace_factor: float = 0.2) -> None:
    if player.outside:
        hours_to_add = int(player.place.get_pace(month=map_game.current_month) * pace_factor * 2)
    else:
        hours_to_add = int(player.place.get_pace(month=map_game.current_month) * pace_factor)
    map_game.add_hours(hours_to_add=hours_to_add)


# Pick up action.
def pick_up(player: Player, item: str) -> str:
    item_name = " ".join(item.split("_")).title()
    if not item:
        return "You need to specify something. PICK UP ITEM"

    if item in player.place.get_items():
        if item not in ITEMS.keys():
            return f"There is no {item_name} here."

        if ITEMS[item].pickable:
            player.add_item(item=item, quantity=1)  # Adding item to inventory.
            player.place.remove_item(item=item)  # Removing item from place.
            return f"You pick up {item_name}."
        return f"You can't pick {item_name}."
    return f"There is no {item_name} here."


def read(player: Player, item: str) -> str:
    item_object = get_item(item_name=item)

    if not player.has(item):
        if item not in player.place.get_items():
            return f"You have not {item} and there is not a {item} here."

    if item is None:
        return f"There is not a {item} here."

    if item_object is None:
        return f"You can't read {item}."

    if not item_object.readable:
        return f"You can't read {item}."

    displays.disp_standard_tw(name=item_object.get_title,
                              message=item_object.readings)

    return f"You have read {item_object.name}."


# Sleep to [morning, afternoon, evening, night].
def sleep_in_bed(player: Player, map_game: Map, time_of_day: int) -> str:
    if "bed" in player.place.get_items():
        map_game.skip_to(time_of_day=time_of_day)
        player.hp = player.hpmax
        return f"You slept until the {TimeOfDay(time_of_day).name.title()}."

    else:
        return "There is no bed here."


# Sell action.
def sell(player: Player, item: str, quantity: int, price: int) -> str:
    inventory = player.inventory
    items = player.inventory.items
    item_name = item.replace("_", " ").title()
    try:
        if items[item] >= quantity:
            player.inventory.discard_item(item=item, quantity=quantity)
            inventory.gold += quantity * price
            return f"You sell {quantity} {item_name}. You earn {quantity * price} gold."

        else:
            return f"You don't have enough {item_name}."

    except KeyError:
        return f"You don't have enough {item_name}."


# Talk.
def talk(npc: Npc, player: Player, map_game: Map) -> str:
    # First message of npc.
    displays.disp_standard_tw(npc.name, npc.messages[0])  # Printing first message.
    npc.hist_messages[0] = True  # Turning True first message of NPC.

    transactions = ""
    while True:
        # Answers for npc.
        if npc.answers.keys():
            displays.disp_talk_answers(npc.answers)  # Printing answers.

            while True:
                try:
                    action_choice = int(input(" " * 4 + "# "))
                    if 0 < action_choice <= len(npc.answers.keys()) + 1:
                        if action_choice == len(npc.answers.keys()) + 1:  # Leave action of talk.
                            # Leave message.
                            if npc.leave_message:
                                displays.disp_standard_tw(npc.name, npc.leave_message)  # Printing leave message.

                            if transactions:
                                return transactions  # Returning transactions if buy or sell actions were done.
                            elif npc.npc_type == NpcTypes.MERCHANT or npc.npc_type == NpcTypes.TAVERN_KEEPER:
                                return "Nothing done."  # If nothing was done.
                            else:
                                return f"You talked with {npc.name.title()}."
                        else:
                            break
                except ValueError:  # Bucle will reset if input is not an intenger.
                    pass

            # Second message of npc.
            displays.disp_standard_tw(npc.name, npc.messages[action_choice])
            npc.hist_messages[action_choice] = True  # Turning True message of NPC.

            # Talking with merchant.
            if npc.npc_type == NpcTypes.MERCHANT or npc.npc_type == NpcTypes.TAVERN_KEEPER:
                print()
                if action_choice == 1:  # Buy option.
                    items, prices, n = [], [], 0

                    for item, value in npc.buy_items.items():
                        item_name = item.replace("_", " ").title()
                        print(f"{' ' * 6}{n + 1}) {item_name} x {value} gold.")
                        items.append(item)
                        prices.append(value)
                        n += 1

                    print(f"{' ' * 6}{n + 1}) Quit.")
                    print()
                    print(f"{' ' * 6}[GOLD: {player.inventory.gold}]\n")

                    while True:
                        try:
                            item = int(input(" " * 4 + "# ")) - 1
                            if 0 <= item < len(items):
                                item_name = items[item].replace('_', ' ').title()
                                if item >= len(items):  # Quit condition.
                                    break
                                print()
                                print(f"{' ' * 4}How many {item_name} do you want to buy?")
                                while True:
                                    try:
                                        quantity = int(input(f"{' ' * 4}# "))
                                        transaction, transaction_status = buy(player, items[item], quantity,
                                                                              prices[item])
                                        transactions += transaction
                                        break
                                    except ValueError:
                                        break
                                break
                            else:
                                break
                        except ValueError:
                            pass

                elif action_choice == 2:  # Sell option.
                    print()
                    items = []
                    prices = []
                    n = 0
                    for item, quantity in player.inventory.items.items():
                        item_object = get_item(item_name=item)

                        if quantity < 1 or item_object.sell_price is None:
                            continue

                        line_text = text_ljust(msg=f"{n + 1}) {item_object.name} x {item_object.sell_price} gold.",
                                               width=30)
                        print(f"{' ' * 6}{line_text[0]} [{player.inventory.items[item]}]")

                        items.append(item)
                        prices.append(item_object.sell_price)
                        n += 1

                    print(f"{' ' * 6}{n + 1}) Quit.")
                    print()
                    print(f"{' ' * 6}GOLD: {player.inventory.gold}.\n")

                    while True:
                        try:
                            item = int(input(f"{' ' * 4}# ")) - 1
                            if 0 <= item < len(items):
                                item_name = items[item].replace("_", " ").title()
                                if item >= len(items):  # Quit condition.
                                    break
                                print()
                                print(f"{' ' * 4}How many {item_name} do you want to sell?")
                                while True:
                                    try:
                                        quantity = int(input(" " * 4 + "# "))
                                        transactions += sell(player, items[item], quantity, prices[item])
                                        break
                                    except ValueError:
                                        pass
                                break
                            else:
                                break
                        except ValueError:
                            pass

                else:
                    return "Nothing done."

            if npc.npc_type == NpcTypes.INNKEEPER:
                print()

                if action_choice == 1:  # Buy room bed.
                    items = []
                    prices = []
                    n = 0
                    for item, value in npc.buy_beds.items():
                        item_name = item.replace("_", " ").title()
                        print(f"{' ' * 6}{n + 1}) {item_name} x {value[0]} gold.")
                        items.append(value[1])
                        prices.append(value[0])
                        n += 1

                    print(f"      {n + 1}) Quit.")
                    print()
                    print(f"{' ' * 6}[GOLD: {player.inventory.gold}]\n")

                    while True:
                        try:
                            item = int(input(f"{' ' * 4}# ")) - 1
                            if 0 <= item < len(items):
                                if item >= len(items):  # Quit condition.
                                    break

                                transaction, transaction_status = buy(player=player,
                                                                      item=items[item],
                                                                      quantity=1,
                                                                      price=prices[item])

                                if transaction_status:
                                    displays.disp_standard_tw(name=npc.name,
                                                              message=["Perfect. Keep this key, until 30 days."])
                                    expiration_date = ITEMS[items[item]].expiration
                                    npc.room_expirations[items[item]] = map_game.estimate_date(days=expiration_date)
                                else:
                                    displays.disp_standard_tw(name=npc.name,
                                                              message=["Mmmm... you don't have enough."])
                                break

                            else:
                                break
                        except ValueError:
                            pass

                if action_choice == 2:  # Buy food.
                    items = []
                    prices = []
                    n = 0
                    for item, value in npc.buy_items.items():
                        item_name = item.replace("_", " ").title()
                        print(f"{' ' * 6}{n + 1}) {item_name}  x {value} gold.")
                        items.append(item)
                        prices.append(value)
                        n += 1

                    print(f"      {n + 1}) Quit.")
                    print()
                    print(f"{' ' * 6}[GOLD: {player.inventory.gold}]\n")

                    while True:
                        try:
                            item = int(input(f"{' ' * 4}# ")) - 1
                            if 0 <= item < len(items):
                                if item >= len(items):  # Quit condition.
                                    break
                                print()
                                item_name = items[item].replace('_', ' ').title()
                                print(f"{' ' * 4}How many {item_name} do you want to buy?")

                                while True:
                                    try:
                                        quantity = int(input(" " * 4 + "# "))
                                        transaction, transaction_status = buy(player=player,
                                                                              item=items[item],
                                                                              quantity=quantity,
                                                                              price=prices[item])
                                        transactions += transaction
                                        break

                                    except ValueError:
                                        break
                                break

                            else:
                                break

                        except ValueError:
                            pass

            if npc.npc_type == NpcTypes.ARTISAN:
                print()
                if action_choice == 1:  # Craft option.
                    items, prices, n = [], [], 0

                    for item, value in npc.crafting_items.items():
                        item_object = ITEMS[item]
                        item_name = item.replace("_", " ").title()
                        print(
                            f"{' ' * 6}{n + 1}) {item_name} x {value} gold. Requires: {item_object.crafting_materials}")
                        items.append(item)
                        prices.append(value)
                        n += 1

                    print(f"      {n + 1}) Quit.")
                    print()
                    print(f"{' ' * 6}[GOLD: {player.inventory.gold}]\n")

                    while True:
                        try:
                            item = int(input(" " * 4 + "# ")) - 1
                            if 0 <= item < len(items):
                                item_name = items[item].replace('_', ' ').title()
                                if item >= len(items):  # Quit condition.
                                    break
                                print()
                                print(f"{' ' * 4}How many {item_name} do you want to craft?")
                                while True:
                                    try:
                                        quantity = int(input(f"{' ' * 4}# "))
                                        transaction, transaction_status = craft(player=player,
                                                                                item=items[item],
                                                                                quantity=quantity)
                                        transactions += transaction
                                        break
                                    except ValueError:
                                        break
                                break
                            else:
                                break
                        except ValueError:
                            pass

                else:
                    return "Nothing done."

        elif npc.name == "whispers":
            return "You heard some whispers. "

        else:
            return f"You talked with {npc.name.title()}."  # Break if the npc has no second message.


# Unequip action.
def unequip(player: Player, item: str) -> str:
    item_name = item.replace("_", " ").title()
    item_object = get_item(item_name=item)

    if not item_object:
        return f"You don't have equipped {item_name}."

    if item_object not in player.equip.values():
        return f"You don't have equipped {item_object.name}."

    player.unequip_item(item=item_object)
    player.inventory.add_item(item=item, quantity=1)
    return f"You have unequip {item_object.name}."


# Use boat.
def use_boat(player: Player, map_game: Map) -> str:
    place = map_game.map_settings[(player.x, player.y)]

    if "boat" in place.get_items() and not player.status == PlayerStatus.SURF.value:
        player.status = PlayerStatus.SURF.value
        place.remove_item(item="boat")

        for k, v in place.description.items():
            if place.get_items().count("boat") < 2:
                place.description[k] = v.replace("Anchored boat gently resting by the shore.", "")

        return "You are in the boat."

    elif player.status == PlayerStatus.SURF.value:
        return "You are already in the boat."

    else:
        return "There is no boat here."


# Use action (general).
def use(player: Player, map_game: Map, item: str) -> tuple[str, bool]:
    if item is None:
        return "You cannot use None.", False

    if item == "gold":
        return f"You can't use {item.replace('_', ' ').title()}.", False

    if item not in player.inventory.items.keys():
        return f"You have no {item.replace('_', ' ').title()}.", False

    if player.inventory.items[item] > 0:
        if "potion" in item:
            if item == "giant_red_potion":
                player.heal(amount=40)

            elif item == "red_potion":
                player.heal(amount=25)

            elif item == "little_red_potion":
                player.heal(amount=10)

            else:
                return "Nothing done.", False

            player.inventory.discard_item(item=item, quantity=1)

            return f"{player.name}'s HP refilled to {player.hp}!", True

        elif "antidote" in item:
            player.heal_poisoning()
            player.inventory.discard_item(item=item, quantity=1)

            return "You have taken the antidote.", True

        elif "powder_keg" in item:
            explosion = False
            for neighbor in map_game.neighbors_from_coord((player.x, player.y)):
                if "rocks" in neighbor.req:
                    neighbor.req.remove("rocks")
                    player.inventory.discard_item(item=item, quantity=1)
                    explosion = True
            if explosion:
                return "You have explode the keg powder on all the rocks.", True
            else:
                return "There is nothing to explode here.", False

        else:
            return "You can't use this item.", False
    else:
        return f"You have no more {item.replace('_', ' ').title()}.", False


# Wait action.
def wait(map_game: Map, time_of_day: int) -> str:
    map_game.skip_to(time_of_day=time_of_day)
    return f"You wait until the {TimeOfDay(time_of_day).name.title()}."
