# Imports.
# Internal imports.
from .. import displays
from ..biome import Biome, Entry
from ..enums import EntryType, PlayerStatus, TimeOfDay
from ..item import Item
from ..map import Map
from ..mob import Mob
from ..player import Player
from ..utils import underscores
from ..world import ITEMS

from .battle import battle
from .explore import explore
from .fish import fish
from .use import use

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
           mob: Mob) -> bool:
    win = battle(players=[player],
                 mapgame=map_game,
                 enemies=[mob],
                 pace_factor=.05)
    return win


# Buy action.
def buy(player: Player,
        item: str,
        quantity: int,
        cost: dict) -> tuple[str, bool]:
    for k, v in cost.items():
        if not player.has(item=k, amount=v * quantity):
            cost_name = underscores(text=k, delete=True).title()
            return f"You don't have enough {cost_name}.", False

    item_name = underscores(text=item, delete=True).title()
    player.add_item(item=item, quantity=quantity)
    for k, v in cost.items():
        player.inventory.discard_item(item=k, quantity=v * quantity)
    return f"You buy {quantity} {item_name}.", True


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
            player.map_labels[y][x] = map_game.map_settings[(x, y)].name[map_game.current_month].upper()

    # Map the boxes within the circular radius.
    for i in range(max(0, player.x - int(exploration_radius)),
                   min(map_game.x_len, player.x + int(exploration_radius) + 1)):
        for j in range(max(0, player.y - int(exploration_radius)),
                       min(map_game.y_len, player.y + int(exploration_radius) + 1)):
            # Checks if the cell is inside de circunference.
            if math.sqrt((player.x - i) ** 2 + (player.y - j) ** 2) <= exploration_radius:
                map_tile(x=i, y=j)

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

    requirements = " ".join(entrie_object.get_req(month=mapgame.current_month)).split("_")
    requirements = " ".join(requirements).title()
    return "You need " + requirements + " to enter.", True


# Equip action.
def equip(player: Player, item: str) -> str:
    if item is None:
        return "You cannot equip this item."

    item_name = item.replace('_', ' ').title()
    item_object = get_item(item_name=item)

    if not item_object:
        return f"You don't have {item_name}."

    if item not in player.inventory.items.keys():
        return f"You don't have {item_object.name}."

    if not item_object.equippable:
        if player.has_slots():
            if player.has_slot_empty():
                player.equip_item(item=item_object)
                return f"You have equip {item_object.name}."
            return "You haven't a slot empty."
        return f"You need a belt to carry this item."

    if player.equip[item_object.body_part] is not None:
        return f"You already have an item equipped. UNEQUIP {item_object.name}."

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
    if (y > 0 and all(req in [*inventory.keys()] + events for req in
                      ms[(x, y - 1)].get_req(month=map_game.current_month)) and player.status
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
            req in [*inventory.keys()] + events for req in
            ms[(x + 1, y)].get_req(month=map_game.current_month)) and player.status
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
            req in [*inventory.keys()] + events for req in
            ms[(x, y + 1)].get_req(month=map_game.current_month)) and player.status
            in ms[(x, y + 1)].get_status(month=map_game.current_month) and mv == "3"):
        if (tl_map[y + 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (
                tl_map[y + 1][x] != "town" and tl_map[y][x] != "town") or (
                tl_map[y][x] == "town" and tl_map[y + 1][x] in ["town", "gates"]):
            player.x, player.y = x, y + 1
            player.set_place(place=map_game.map_settings[(player.x, player.y)])
            map_game.add_hours(hours_to_add=int(player.place.get_pace(month=map_game.current_month) * pace_factor))
            return "You moved South.", False

    # Move West.
    if (x > 0 and all(req in [*inventory.keys()] + events for req in
                      ms[(x - 1, y)].get_req(month=map_game.current_month)) and player.status
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
def sell(player: Player, item: str, quantity: int, price: int) -> tuple[str, bool]:
    item_name = underscores(text=item, delete=True).title()
    if player.has(item=item, amount=quantity):
        earning = quantity * price
        player.inventory.discard_item(item=item, quantity=quantity)
        player.inventory.add_item(item="gold", quantity=earning)
        return f"You sell {quantity} {item_name}. You earn {earning} gold.", True
    return f"You don't have enough {item_name}.", False


# Unequip action.
def unequip(player: Player, item: str) -> str:
    if item is None:
        f"You don't have equipped {item}."

    item_name = item.replace("_", " ").title()
    item_object = player.get_equiped_item(item=item)

    if not item_object:
        return f"You don't have equipped {item_name}."

    if item_object.id in [slot_item.id for slot_item in player.belt.get_slot_items()]:
        player.unequip_item(item=item_object)
        return f"You have unequip {item_object.name}."

    player.unequip_item(item=item_object)
    if item_object.equippable:
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


# Wait action.
def wait(map_game: Map, time_of_day: int) -> str:
    map_game.skip_to(time_of_day=time_of_day)
    return f"You wait until the {TimeOfDay(time_of_day).name.title()}."
