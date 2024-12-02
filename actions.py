# Imports.
# Internal imports.
import globals
from biome import Biome, Entry
from displays import disp_battle, disp_talk_answers, disp_talk_tw
from enums import EntryType, NpcTypes, PlayerStatus, TimeOfDay
from item import Item
from map import Map
from npc import Npc
from player import Player
from utils import reset_map, text_ljust

# External imports.
import math
import random


# ----------------------------------------------------------------------------------------------------
# Utiliy functions.
def get_item(item_name: str) -> Item:
    if item_name in globals.ITEMS.keys():
        return globals.ITEMS[item_name]


# ----------------------------------------------------------------------------------------------------


# Battle action.
def battle(player: Player, map_game: Map, enemy: dict, pace_factor: float = 0.05) -> tuple[bool, bool, int]:
    screen = "Defeat the enemy!"
    play = True
    menu = False
    fight = True

    hours_to_add = 0
    while fight:
        disp_battle(player, enemy, screen)
        choice_action = input(" # ")  # User choice action.
        object_used = True
        screen = "."  # Clearing text output screen.
        hours_to_add += player.place.pace * pace_factor

        if choice_action == "0":  # Escape option.
            escape = random.choices([True, False], [enemy["esc"], 100 - enemy["esc"]], k=1)
            if escape[0]:
                fight = False
                screen = "You have escaped."
            else:
                screen = "You have not escaped."

        elif choice_action == "1":  # Attack option.
            if player.precision * (1 - enemy["eva"]) > random.random():
                USER_DMG = max(int(int(player.attack) - int(enemy["def"])), 0)
                enemy["hp"] -= USER_DMG
                screen = " " + player.name + " dealt " + str(USER_DMG) + " damage to the " + enemy["name"] + "."
            else:
                screen = " " + player.name + " fail the attack."

        elif choice_action in ["2", "3"]:  # Use object action.
            if choice_action == "2":
                screen, object_used = use(player, map_game=map_game, item=player.slot1)
            if choice_action == "3":
                screen, object_used = use(player, map_game=map_game, item=player.slot2)

        # Enemy attack.
        if enemy["hp"] > 0 and choice_action in ["0", "1", "2", "3"]:
            if enemy["pre"] * (1 - player.evasion) > random.random() and object_used:
                ENEMY_ATK = [[enemy["atk"], enemy["atk"] * enemy["c_coef"]],
                             [100 - enemy["c_chance"], enemy["c_chance"]]]
                ENEMY_DMG = max(int(int(random.choices(ENEMY_ATK[0], ENEMY_ATK[1], k=1)[0]) - int(player.defense)), 0)
                player.hp -= ENEMY_DMG
                screen += "\n " + enemy["name"] + " dealt " + str(ENEMY_DMG) + " damage to " + player.name + "."
                if enemy["poison"] > 0 and enemy["c_poison"] > random.random() and player.poison == 0:
                    player.poison = enemy["poison"]
                    screen += "\n " + enemy["name"] + " has poisoned you."
            else:
                screen += "\n " + enemy["name"] + " fail the attack."
        input(" > ")

        # Logic of fight status or result.
        # Lose.
        if player.hp <= 0:
            disp_battle(player, enemy, screen)
            screen += "\n " + enemy["name"] + " defeated " + player.name + "..."
            disp_battle(player, enemy, screen)
            input(" > ")

            # Setting reinit.
            play = False
            menu = True
            player.hp, player.x, player.y = int(player.hpmax), player.x_cp, player.y_cp
            player.status = 0
            player.exp = 0
            reset_map(ms=map_game.map_settings, keys=[(2, 1), (6, 2)])

            print(" GAME OVER")
            input(" > ")
            return play, menu, 0

        # Win.
        if enemy["hp"] <= 0:
            screen += "\n " + "You defeated the " + enemy["name"] + "!"
            fight = False
            map_game.add_hours(hours_to_add=int(hours_to_add))

            # Drop items logic and exp gain.
            if enemy["items"]:
                drop_quantity = random.randint(1, len(enemy["items"])) - 1
                drop_items = list(
                    set(random.choices([*enemy["items"].keys()], cum_weights=enemy["dc_items"], k=drop_quantity)))

                for item in drop_items:
                    if item == "gold":
                        player.inventory.gold += enemy["items"][item]
                        screen += "\n You've found " + str(enemy["items"][item]) + " " + item.replace("_",
                                                                                                      " ").title() + "."
                    elif item != "none" and item in player.inventory.items.keys():
                        player.inventory.items[item] += enemy["items"][item]
                        screen += "\n You've found " + str(enemy["items"][item]) + " " + item.replace("_",
                                                                                                      " ").title() + "."
                    elif item != "none":
                        player.inventory.items[item] = enemy["items"][item]

            screen += "\n You have gained " + str(enemy["exp"]) + " experience."

            if player.add_exp(enemy["exp"]):
                screen += "You have lvl up. ASSIGN Strength/Agility/Vitality. You can assign 3 points."

    disp_battle(player, enemy, screen)
    input(" > ")

    return play, menu, 1


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
    inventory = player.inventory
    items = player.inventory.items
    if inventory.gold >= price * quantity:
        try:
            items[item] += quantity

        except KeyError:
            items[item] = quantity
        inventory.gold -= price * quantity

        return f"You buy {quantity} {item_name}.", True

    else:
        return "You don't have enough gold.", False


# Check action.
def check(player: Player = None, item: str = None, inventory: bool = False) -> str:
    if player is None or item is None:
        return f"What do you want to check? CHECK ITEM for items at places or CHECK INV ITEM for items in the inventory."

    if item in player.place.items or (inventory and item in player.inventory.items.keys()):
        if item in globals.ITEMS.keys():
            text = globals.ITEMS[item].description

        else:
            text = f"You observe nothing."

    elif item == "":
        text = f"What do you want to check? CHECK ITEM for items at places or CHECK INV ITEM for items at the inventory."

    elif item in globals.ITEMS.keys():
        text = f"There is no {globals.ITEMS[item].name} here."

    else:
        text = f"There is no {item.title()} here."

    return text


def craft(player: Player, item: str) -> str:
    if item not in globals.ITEMS:
        return "This item cannot be craft."

    items = player.inventory.items
    item_object = globals.ITEMS[item]
    item_name = item_object.name

    for mat, mat_amount in item_object.crafting_materials.items():
        material_name = mat.replace("_", " ").title()
        if mat not in items:
            return f"You haven't {material_name} to craft {item_name}. You need {mat_amount} {material_name}."
        if items[mat] < mat_amount:
            return f"You haven't enough {material_name} to craft {item_name}. You need {mat_amount} {material_name}."

    for mat, mat_amount in item_object.crafting_materials.items():
        player.inventory.discard_item(item=mat, quantity=mat_amount)

    player.inventory.add_item(item=item, quantity=1)

    return f"You crafted a {item_object.name}."


# Draw map action.
def draw_map(player: Player, map_game: Map, pace_factor: float = 0.5, exploration_radius: float = None) -> str:
    if not player.place.draw_map:
        return "You can't draw map here. You can't explore for it."

    if exploration_radius is None:
        exploration_radius = player.exploration_radius

    player.map[player.y][player.x] = map_game.map_settings[(player.x, player.y)].color

    # Helper function to map specific coordinates.
    def map_tile(x: int, y: int):
        if 0 <= x < map_game.x_len and 0 <= y < map_game.y_len:
            player.map[y][x] = map_game.map_settings[(x, y)].color

    # Map the boxes within the circular radius.
    for i in range(max(0, player.x - int(exploration_radius)),
                   min(map_game.x_len, player.x + int(exploration_radius) + 1)):
        for j in range(max(0, player.y - int(exploration_radius)),
                       min(map_game.y_len, player.y + int(exploration_radius) + 1)):
            # Verificar si la casilla está dentro del círculo
            if math.sqrt((player.x - i) ** 2 + (player.y - j) ** 2) <= exploration_radius:
                map_tile(i, j)

    # Add time based on venue tempo and pace factor.
    hours_to_add = int(player.place.pace * pace_factor)
    map_game.add_hours(hours_to_add=hours_to_add)

    return "You have explored the area and mapped it out."


# Drop action.
def drop(player: Player, item: str, quantity: int = 1) -> str:
    item_name = item.replace("_", " ")
    item_object = globals.ITEMS[item]

    if not item_object.droppable:
        return f"You can't drop {item_object.name}."

    if player.inventory.drop_item(item=item, quantity=quantity):
        return f"You drop {quantity} {item_name.title()}."

    else:
        return f"You don't have {quantity} {item_name}."


# Enter action.
def enter(player: Player, entrie: str, map_game: Map) -> tuple[str, bool]:
    if entrie is None:
        return "You need to specify the name more clearly.", True

    objects = [*player.inventory.items.keys()] + [*player.events.keys()]
    entry_name = entrie.replace("_", " ").title()

    if entrie not in player.place.entries.keys():
        return f"There is not a {entry_name} here.", True

    entrie_object = player.place.entries[entrie]
    if type(entrie_object) == Entry and not entrie_object.hide["visibility"]:
        return f"There is not a {entry_name} here.", True

    elif all(req in objects for req in entrie_object.req):
        if type(entrie_object) == Entry:
            player.outside = False
        elif type(entrie_object) == Biome:
            player.x, player.y = entrie_object.x, entrie_object.y
            player.outside = True
        entrie_name = entrie_object.name
        player.set_place(entrie_object)
        return f"You have enter to the {entrie_name}.", False

    else:
        requirements = " ".join(entrie_object.req).split("_")
        requirements = " ".join(requirements).title()
        return "You need " + requirements + " to enter.", True


# Equip action.
def equip(player: Player, item: str) -> str:
    item_name = item.replace('_', ' ').title()
    item_object = get_item(item_name=item)

    if item not in player.inventory.items.keys() or item_object is None:
        return f"You don't have {item_name}."

    elif not item_object.equippable:
        return f"You can't equip {item_object.name}."

    elif player.equip[item_object.body_part] is not None:
        return f"You already have an item equipped. UNEQUIP {item_object.body_part.name}."

    else:
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

    return f"You left the {player.last_place.name}.", False


# Explore action.
def explore(player: Player, map_game: Map, pace_factor: float = 0.5) -> str:
    if player.place.entries is None:
        map_game.add_hours(hours_to_add=int(player.place.pace * pace_factor))
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
                map_game.add_hours(hours_to_add=int(player.place.pace * pace_factor))
                return f"You have found a {entrie.name}."
            map_game.add_hours(hours_to_add=int(player.place.pace * pace_factor))
            return "You explore the zone but you found nothing."
    map_game.add_hours(hours_to_add=int(player.place.pace * pace_factor))
    return f"You explore the zone but you found nothing."


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
        map_game.map_settings[(x, y)].description = map_game.map_settings[(x, y)].description.replace(
            "Seaside with swaying palm trees, echoing waves, and vibrant life.",
            "Seaside with anchored boat, echoing waves and vibrant coastal life.")

        if map_game.map_settings[(x, y)].description == "":
            map_game.map_settings[(x, y)].description = ("Seaside with anchored boat, echoing waves and vibrant"
                                                                 " coastal life.")

        map_game.add_hours(hours_to_add=int(player.place.pace * pace_factor))
        return "You have land."

    else:
        if player.status == PlayerStatus.SURF.value:
            return "You can't land here."

        else:
            return "You aren't in a boat."


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
    if (y > 0 and all(req in [*inventory.keys()] + events for req in ms[(x, y - 1)].req) and player.status
            in ms[(x, y - 1)].status and mv == "1"):
        if (tl_map[y - 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (
                tl_map[y - 1][x] != "town" and tl_map[y][x] != "town") or (
                tl_map[y][x] == "town" and tl_map[y - 1][x] in ["town", "gates"]):
            player.x, player.y = x, y - 1
            player.set_place(place=map_game.map_settings[(player.x, player.y)])
            map_game.add_hours(hours_to_add=int(player.place.pace * pace_factor))
            return "You moved North.", False

    # Move East.
    if (x < map_height and all(
            req in [*inventory.keys()] + events for req in ms[(x + 1, y)].req) and player.status
            in ms[(x + 1, y)].status and mv == "2"):
        if (tl_map[y][x + 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (
                tl_map[y][x + 1] != "town" and tl_map[y][x] != "town") or (
                tl_map[y][x] == "town" and tl_map[y][x + 1] in ["town", "gates"]):
            player.x, player.y = x + 1, y
            player.set_place(place=map_game.map_settings[(player.x, player.y)])
            map_game.add_hours(hours_to_add=int(player.place.pace * pace_factor))
            return "You moved East.", False

    # Move South.
    if (y < map_width and all(
            req in [*inventory.keys()] + events for req in ms[(x, y + 1)].req) and player.status
            in ms[(x, y + 1)].status and mv == "3"):
        if (tl_map[y + 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (
                tl_map[y + 1][x] != "town" and tl_map[y][x] != "town") or (
                tl_map[y][x] == "town" and tl_map[y + 1][x] in ["town", "gates"]):
            player.x, player.y = x, y + 1
            player.set_place(place=map_game.map_settings[(player.x, player.y)])
            map_game.add_hours(hours_to_add=int(player.place.pace * pace_factor))
            return "You moved South.", False

    # Move West.
    if (x > 0 and all(req in [*inventory.keys()] + events for req in ms[(x - 1, y)].req) and player.status
            in ms[(x - 1, y)].status and mv == "4"):
        if (tl_map[y][x - 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (
                tl_map[y][x - 1] != "town" and tl_map[y][x] != "town") or (
                tl_map[y][x] == "town" and tl_map[y][x - 1] in ["town", "gates"]):
            player.x, player.y = x - 1, y
            player.set_place(place=map_game.map_settings[(player.x, player.y)])
            map_game.add_hours(hours_to_add=int(player.place.pace * pace_factor))
            return "You moved West.", False

    return "You can't move there.", True


# Look around action.
def look_around(player: Player, map_game: Map, pace_factor: float = 0.2) -> None:
    hours_to_add = int(player.place.pace * pace_factor)
    map_game.add_hours(hours_to_add=hours_to_add)


# Pick up action.
def pick_up(player: Player, item: str) -> str:
    item_name = " ".join(item.split("_")).title()
    if item in player.place.items:
        if item in globals.ITEMS.keys() and globals.ITEMS[item].pickable:
            player.inventory.add_item(item=item, quantity=1)  # Adding item to inventory.
            player.place.items.remove(item)  # Removing item from place.

            return f"You pick up {item_name}."

        else:
            return f"You can't pick {item_name}."
    else:
        return f"There is no {item_name} here."


# Sleep to [morning, afternoon, evening, night].
def sleep_in_bed(player: Player, map_game: Map, time_of_day: int) -> str:
    if "bed" in player.place.items:
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
            items[item] -= quantity
            inventory.gold += quantity * price
            return f"You sell {quantity} {item_name}. You earn {quantity * price} gold."

        else:
            return f"You don't have enough {item_name}."

    except KeyError:
        return f"You don't have enough {item_name}."


# Talk.
def talk(npc: Npc, player: Player, map_game: Map) -> str:
    # First message of npc.
    disp_talk_tw(npc, npc.messages[0])  # Printing first message.
    npc.hist_messages[0] = True  # Turning True first message of NPC.

    transactions = ""
    while True:
        # Answers for npc.
        if npc.answers.keys():
            disp_talk_answers(npc.answers)  # Printing answers.

            while True:
                try:
                    action_choice = int(input(" " * 4 + "# "))
                    if 0 < action_choice <= len(npc.answers.keys()) + 1:
                        if action_choice == len(npc.answers.keys()) + 1:  # Leave action of talk.
                            # Leave message.
                            if npc.leave_message:
                                disp_talk_tw(npc, npc.leave_message)  # Printing leave message.

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
            disp_talk_tw(npc, npc.messages[action_choice])
            npc.hist_messages[action_choice] = True  # Turning True message of NPC.

            # Talking with merchant.
            if npc.npc_type == NpcTypes.MERCHANT or npc.npc_type == NpcTypes.TAVERN_KEEPER:
                print()
                if action_choice == 1:  # Buy option.
                    items, prices, n = [], [], 0

                    for item, value in npc.buy_items.items():
                        item_name = item.replace("_", " ").title()
                        if item != "quit":
                            print(f"{' ' * 6}{n + 1}) {item_name} x {value} gold.")
                        else:
                            print(f"{' ' * 6}{n + 1}) {item_name}")
                        items.append(item)
                        prices.append(value)
                        n += 1
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
                        print(f"{' ' * 6}{line_text[0]}[{player.inventory.items[item]}]")

                        items.append(item)
                        prices.append(item_object.sell_price)
                        n += 1
                    print(f"{' ' * 6}{n + 1}) Quit.")
                    items.append("quit")
                    print()
                    print(f"{' ' * 6}GOLD: {player.inventory.gold}.\n")

                    while True:
                        try:
                            item = int(input(f"{' ' * 4}# ")) - 1
                            if 0 <= item < len(items):
                                item_name = items[item].replace("_", " ").title()
                                if item >= len(items) - 1:  # Quit condition.
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
                        if item != "quit":
                            print(f"{' ' * 6}{n + 1}) {item_name} x {value[0]} gold.")

                        else:
                            print(f"{' ' * 6}{n + 1}) {item_name}")
                        items.append(value[1])
                        prices.append(value[0])
                        n += 1
                    print()
                    print(f"{' ' * 6}[GOLD: {player.inventory.gold}]\n")

                    while True:
                        try:
                            item = int(input(f"{' ' * 4}# ")) - 1
                            if 0 <= item < len(items):
                                if item >= len(items) - 1:  # Quit condition.
                                    break

                                transaction, transaction_status = buy(player=player,
                                                                      item=items[item],
                                                                      quantity=1,
                                                                      price=prices[item])

                                if transaction_status:
                                    disp_talk_tw(npc=npc,
                                                 message=["Perfect. Keep this key, until 30 days."])
                                    expiration_date = globals.ITEMS[items[item]].expiration
                                    npc.room_expirations[items[item]] = map_game.estimate_date(days=expiration_date)
                                else:
                                    disp_talk_tw(npc=npc,
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
                        if item != "quit":
                            print(f"{' ' * 6}{n + 1}) {item_name}  x {value} gold.")

                        else:
                            print(f"{' ' * 6}{n + 1}) {item_name}")
                        items.append(item)
                        prices.append(value)
                        n += 1
                    print()
                    print(f"{' ' * 6}[GOLD: {player.inventory.gold}]\n")

                    while True:
                        try:
                            item = int(input(f"{' ' * 4}'# '")) - 1
                            if 0 <= item < len(items):
                                if item >= len(items) - 1:  # Quit condition.
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
            pass

        elif npc.name == "whispers":
            return "You heard some whispers. "

        else:
            return f"You talked with {npc.name.title()}."  # Break if the npc has no second message.


# Unequip action.
def unequip(player: Player, item: str) -> str:
    item_name = item.replace("_", " ").title()
    item_object = get_item(item_name=item)

    if item_object not in player.equip.values() or item_object is None:
        return f"You don't have equipped {item_name}."

    else:
        player.unequip_item(item=item_object)
        player.inventory.add_item(item=item, quantity=1)
        return f"You have unequip {item_object.name}."


# Use boat.
def use_boat(player: Player, map_game: Map) -> str:
    place = map_game.map_settings[(player.x, player.y)]

    if "boat" in place.items and player.status != PlayerStatus.SURF.value:
        player.status = PlayerStatus.SURF.value
        place.items.remove("boat")

        if f"{(player.x, player.y)}" == (6, 2):
            description = """Seaside with swaying palm trees, echoing waves, and vibrant life. A solitary figure stands 
            at the water's edge, gazing out into the vastness of the sea, captivated by the rhythmic dance of the waves
             and the boundless horizon stretching before them."""
            place.description = description

        else:
            place.description = "Seaside with swaying palm trees, echoing waves, and vibrant life."

        return "You are in the boat."

    elif player.status == PlayerStatus.SURF.value:
        return "You are already in the boat."

    else:
        return "There is no boat here."


# Use action (general).
def use(player: Player, map_game: Map, item: str) -> tuple[str, bool]:
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

            elif item == "litle_red_potion":
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
