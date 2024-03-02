# Imports.
# External imports.
import random

# Internal imports.
from displays import disp_battle, disp_talk_util
import globals
from player import Player
from utils import day_est, typewriter, clear, text_ljust, coast_reset


# Battle action.
def battle(player: Player(), enemy: dict, ms: dict):

    screen = "Defeat de enemy!"
    play = True
    menu = False
    fight = True

    while fight:
        disp_battle(player, enemy, screen)
        choice_action = input(" # ")  # User choice action.
        object_used = True
        screen = "."  # Clearing text output screen.

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
                fast_object = player.slot1
            if choice_action == "3":
                fast_object = player.slot2
            screen, object_used = use(player, fast_object)

        # Enemy attack.
        if enemy["hp"] > 0 and choice_action in ["0", "1", "2", "3"]:
            if enemy["pre"] * (1 - player.evasion) > random.random() and object_used:
                ENEMY_ATK = [[enemy["atk"], enemy["atk"] * enemy["c_coef"]], [100 - enemy["c_chance"], enemy["c_chance"]]]
                ENEMY_DMG = max(int(int(random.choices(ENEMY_ATK[0], ENEMY_ATK[1], k=1)[0]) - int(player.defense)), 0)
                player.hp -= ENEMY_DMG
                screen += "\n " + enemy["name"] + " dealt " + str(ENEMY_DMG) + " damage to " + player.name + "."
            else:
                screen += "\n " + enemy["name"] + " fail the attack."
        input(" > ")

        # Logic of fight status or result.
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
            coast_reset(ms=ms, keys=["(2, 1)", "(6, 2)"])

            print(" GAME OVER")
            input(" > ")
            return play, menu, 0

        if enemy["hp"] <= 0:
            screen += "\n " + "You defeated the " + enemy["name"] + "!"
            fight = False

            # Drop items logic.
            player.exp += enemy["exp"]
            if enemy["items"]:
                drop_quantity = random.randint(1, len(enemy["items"])) - 1
                drop = list(set(random.choices([*enemy["items"].keys()], cum_weights=enemy["dc_items"], k=drop_quantity)))

                for item in drop:
                    if item == "gold":
                        player.inventory.gold += enemy["items"][item]
                        screen += "\n You've found " + str(enemy["items"][item]) + " " + item.replace("_", " ").title() + "."
                    elif item != "none" and item in player.inventory.items.keys():
                        player.inventory.items[item] += enemy["items"][item]
                        screen += "\n You've found " + str(enemy["items"][item]) + " " + item.replace("_", " ").title() + "."
                    elif item != "none":
                        player.inventory.items[item] = enemy["items"][item]

            screen += "\n You have gained " + str(enemy["exp"]) + " experience."

    disp_battle(player, enemy, screen)
    input(" > ")
    return play, menu, 1


# Buy action.
def buy(player: Player(), item: str, quantity: int, price: int) -> str:
    inventory = player.inventory
    items = player.inventory.items
    if inventory.gold >= price * quantity:
        try:
            items[item] += quantity
        except KeyError:
            items[item] = quantity
        inventory.gold -= price * quantity
        return "You buy " + str(quantity) + " " + item.replace("_", " ").title() + "."
    else:
        return "You don't have enough gold."


# Check action.
def check(x: int, y: int, ms: dict, item: str) -> str:
    text = ""
    if item in ms[str((x, y))]["items"]:
        if item == "bed":
            text = "Comfortable resting surface for sleep and relaxation."
        elif item == "boat":
            text = "Small wooden boat gently rocks on calm water, weathered by time and adventures."
        elif item == "origami flowers":
            text = "Paper flowers, seem to have something inside the stem, but you can't get it out with your fingers," \
                   " you need a long stick."
        else:
            text = "You observe nothing."
    elif item == "":
        text = "What do you     want to check? CHECK ITEM"
    else:
        text = "There is no " + item.title() + " here."

    return text


# Drop action.
def drop(player: Player(), item_name: str, quantity: int = 1) -> tuple[str, dict]:
    item = item_name.replace(" ", "_")
    items = player.inventory.items
    try:
        if items[item] >= int(quantity) and item not in ["red_potion", "walk"]:
            items[item] -= int(quantity)
            if items[item] <= 0:
                del items[item]
            return "You drop " + str(quantity) + " " + item_name.title() + ".", player
        else:
            return "You don't have " + str(quantity) + " " + item_name.title() + ".", player
    except KeyError:
        return "You don't have " + item_name.title() + ".", player


# Enter action.
def enter(x: int, y: int, entrie: str, player: Player()) -> tuple[str, int, int, bool]:
    if entrie == "castle":
        return "You cannot enter here.", x, y, False

    if entrie == "cathedral":
        return "You cannot enter here.", x, y, False

    elif entrie == "cave":
        if (x, y) == (13, 0):
            if "torch" in player.inventory.items.keys() and player.inventory.items["torch"] > 0:
                if random.randint(0, 100) <= 10:
                    return "You have crossed the cave without any problems.", 19, 0, False
                else:
                    return "You have crossed the cave.", 19, 0, True
            else:
                return "You need a torch to enter.", x, y, False

        if (x, y) == (19, 0):
            if "torch" in player.inventory.items.keys() and player.inventory.items["torch"] > 0:
                if random.randint(0, 100) <= 10:
                    return "You have crossed the cave without any problems.", 13, 0, False
                else:
                    return "You have crossed the cave.", 13, 0, True
            else:
                return "You need a torch to enter.", x, y, False

    elif entrie == "inn":
        pass

    else:
        return "There is not a " + entrie + " here.", x, y, False


# Equip action.
def equip(player: Player(), item_name: str) -> str:
    item = item_name.replace(" ", "_").lower()
    if item in player.inventory.items.keys() and player.inventory.items[item] > 0 and item in globals.ITEMS_EQUIP.keys():
        body_part = globals.ITEMS_EQUIP[item]["body"]
        if player.equip[body_part] == "None":
            player.equip[body_part] = item
            player.inventory.items[item] -= 1
            return "You have equip " + item_name.title() + "."
        else:
            return "You already have an item equipped. UNEQUIP " + player.equip[body_part].title() + "."
    elif item not in player.inventory.items.keys() or player.inventory.items[item] < 1:
        return "You don't have " + item_name.title() + "."
    elif item not in globals.ITEMS_EQUIP.keys():
        return "You can't equip " + item_name.title() + "."


# Explore action.
def explore(x: int, y: int, set_map: dict):
    if (x, y) == (13, 0) and "cave" not in set_map[str((x, y))]["entries"]:
        set_map[str((x, y))]["entries"].append("cave")
        return "You have found a cave.", set_map
    else:
        return "You explore the zone but you found nothing.", set_map


# Heal action.
def heal(name: str, health: int, healthmax: int, amount: int) -> tuple[str, int]:
    if health + amount < healthmax:
        health += amount
    else:
        health = healthmax
    return name + "'s HP refilled to " + str(health) + "!", health


# Land.
def land(x: int, y: int, player: Player(), set_map: dict, tl_map: list) -> tuple[str, dict]:
    if player.status == 1 and tl_map[y][x] not in ["sea", "river"]:
        player.status = 0
        set_map[str((x, y))]["items"].append("boat")
        try:
            set_map[str((x, y))]["d"] = globals.MAP_SETTING[str((x, y))]["d"]
        except KeyError:
            set_map[str((x, y))]["d"] = "Seaside with anchored boat, echoing waves and vibrant coastal life."
        return "You have land.", set_map
    else:
        if player.status == 1:
            return "You can't land here.", set_map
        else:
            return "You aren't in a boat.", set_map


# Move function.
def move(
        x: int, y: int, map_heigt: int, map_width: int, player: Player(),
        tl_map: list, mv: str, ms: dict) -> tuple[str, int, int, int, bool]:
    inventory = player.inventory.items
    hs = 8
    # Move North.
    if y > 0 and all(req in [*inventory.keys()] for req in ms[str((x, y - 1))]["r"]) and player.status in ms[str((x, y - 1))]["s"] and mv == "1":
        if (tl_map[y - 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y - 1][x] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y - 1][x] in ["town", "gates"]):
            return "You moved North.", x, y - 1, hs, False
    # Move East.
    if x < map_heigt and all(req in [*inventory.keys()] for req in ms[str((x + 1, y))]["r"]) and player.status in ms[str((x + 1, y))]["s"] and mv == "2":
        if (tl_map[y][x + 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y][x + 1] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y][x + 1] in ["town", "gates"]):
            return "You moved East.", x + 1, y, hs, False

    # Move South.
    if y < map_width and all(req in [*inventory.keys()] for req in ms[str((x, y + 1))]["r"]) and player.status in ms[str((x, y + 1))]["s"] and mv == "3":
        if (tl_map[y + 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y + 1][x] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y + 1][x] in ["town", "gates"]):
            return "You moved South.", x, y + 1, hs, False

    # Move West.
    if x > 0 and all(req in [*inventory.keys()] for req in ms[str((x - 1, y))]["r"]) and player.status in ms[str((x - 1, y))]["s"] and mv == "4":
        if (tl_map[y][x - 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y][x - 1] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y][x - 1] in ["town", "gates"]):
            return "You moved West.", x - 1, y, hs, False
    return "You can't move there.", x, y, hs, True


# Sleep to [morning, afternoon, evening, night].
def sleep_in_bed(x: int, y: int, set_map: dict, hp, hpmax, actual_hs, opt: str) -> tuple[str, int, int, str]:
    if opt not in ["morning", "afternoon", "evening", "night"]:
        hs, d_moment = day_est(actual_hs, 0)
        return "This is not posible.", hp, hs, d_moment
    else:
        if "bed" in set_map[str((x, y))]["items"]:
            if opt == "morning":
                return "You slept until the morning.", hpmax, 6, "MORNING"
            elif opt == "afternoon":
                return "You slept until the afternoon.", hpmax, 12, "AFTERNOON"
            elif opt == "evening":
                return "You slept until the evening.", hpmax, 18, "EVENING"
            else:
                return "You slept until the night.", hpmax, 22, "NIGHT"
        else:
            hs, d_moment = day_est(actual_hs, 0)
            return "There is no bed here.", hp, hs, d_moment


# Sell action.
def sell(player: Player(), item: str, quantity: int, price: int) -> str:
    inventory = player.inventory
    items = player.inventory.items
    try:
        if items[item] >= quantity:
            items[item] -= quantity
            inventory.gold += quantity * price
            return "You sell " + str(quantity) + " " + item.replace("_", " ").title() + ". You earn " + str(quantity * price) + " gold."
        else:
            return "You don't have enough " + item.replace("_", " ").title() + "."
    except KeyError:
        return "You don't have enough " + item.replace("_", " ").title() + "."


# Talk.
def talk(npc: dict, npc_name: str, player: Player()) -> str:
    clear()
    # First message of npc.
    for line in npc[0]:
        disp_talk_util(npc_name)

        lines = text_ljust(line, width=70)
        for text in lines:
            typewriter(" " * 4 + text)
            print()

        input(" " * 4 + "> ")
    npc[3][0] = True  # Turning True first message of NPC.

    transactions = ""
    while True:
        # Answers for npc.
        if npc[1]:
            print()
            for i, res in enumerate(npc[1]):
                print(" " * 4 + str(i + 1), ") " + res[0].capitalize() + ".")
            print(" " * 4 + str(i + 2), ") Leave.")
            print()

            while True:
                try:
                    action_choice = int(input(" " * 4 + "# ")) - 1
                    if 0 <= action_choice <= len(npc[1]):
                        if action_choice == len(npc[1]):
                            if transactions:
                                return transactions
                            else:
                                return "Nothing done."
                        npc[3][action_choice + 1] = True  # Turning True response message of NPC.
                        break
                except ValueError:
                    pass

            # Second message of npc.
            for line in npc[1][action_choice][1]:
                disp_talk_util(npc_name)

                lines = text_ljust(line, width=70)
                for text in lines:
                    typewriter(" " * 4 + text)
                    print()

                input(" " * 4 + "> ")

            # Talking with merchant.
            if "merchant" in npc_name:
                print()
                if npc[1][action_choice][0] == "buy":
                    items = []
                    prices = []
                    n = 0
                    for item, value in globals.NPC[npc_name][2][0].items():
                        if item != "quit":
                            print(" " * 6 + str(n + 1) + ") " + item.replace("_", " ").title() + " x " + str(value) + " gold.")
                        else:
                            print(" " * 6 + str(n + 1) + ") " + item.replace("_", " ").title())
                        items.append(item)
                        prices.append(value)
                        n += 1
                    print()
                    print(" " * 6 + "[GOLD: " + str(player.inventory.gold) + "]\n")

                    while True:
                        try:
                            item = int(input(" " * 4 + "# ")) - 1
                            if 0 <= item < len(items):
                                if item >= len(items) - 1:  # Quit condition.
                                    break
                                print()
                                print(" " * 4 + "How many " + items[item].replace("_", " ").title() + " do you want to buy?")
                                while True:
                                    try:
                                        quantity = int(input(" " * 4 + "# "))
                                        transactions += buy(player, items[item], quantity, prices[item])
                                        break
                                    except ValueError:
                                        break
                                break
                            else:
                                break
                        except ValueError:
                            pass

                elif npc[1][action_choice][0] == "sell":
                    print()
                    items = []
                    prices = []
                    n = 0
                    for item, value in {key: globals.ITEMS_SELL[key] for key in set(player.inventory.items.keys()).intersection(set(globals.ITEMS_SELL.keys())) if player.inventory.items[key] > 0}.items():
                        if item != "quit":
                            line_text = text_ljust(str(n + 1) + ") " + item.replace("_", " ").title() + " x " + str(value) + " gold.", 30)
                            print(" " * 6 + line_text[0] + "[" + str(player.inventory.items[item]) + "]")
                        else:
                            print(" " * 6 + str(n + 1) + ") " + item.replace("_", " "))
                        items.append(item)
                        prices.append(value)
                        n += 1
                    print(" " * 6 + str(n + 1) + ") Quit.")
                    items.append("quit")
                    print()
                    print(" " * 6 + "GOLD: " + str(player.inventory.gold) + ".\n")

                    while True:
                        try:
                            item = int(input(" " * 4 + "# ")) - 1
                            if 0 <= item < len(items):
                                if item >= len(items) - 1:  # Quit condition.
                                    break
                                print()
                                print(" " * 4 + "How many " + items[item].replace("_", " ").title() + " do you want to sell?")
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

            else:
                return  "You talked with " + npc_name.title() + "."

        else:
            return "You talked with " + npc_name.title() + "."  # Break if the npc has no second message.


# Unequip action.
def unequip(player: Player(), item_name: str) -> str:
    item = item_name.replace(" ", "_").lower()
    item_name = item_name.replace("_", " ").title()
    if item in player.equip.values():
        body_part = globals.ITEMS_EQUIP[item]["body"]
        player.equip[body_part] = "None"
        try:
            player.inventory.items[item] += 1
            return "You have unequip " + item_name + "."
        except KeyError:
            player.inventory.items[item] = 1
            return "You have unequip " + item_name + "."
    else:
        return "You don't have " + item_name + " equipped."


# Use action (general).
def use(player: Player(), obj: str) -> tuple[str, bool]:
    object_used = False
    item = obj.replace(" ", "_").lower()
    if item == "gold":
        return "You can't use " + item.replace("_", " ").title() + ".", object_used
    if item not in player.inventory.items.keys():
        return "You have no " + item.replace("_", " ").title() + ".", object_used
    if player.inventory.items[item] > 0:
        if "potion" in item:
            if item == "giant_red_potion":
                text, player.hp = heal(player.name, player.hp, player.hpmax, 40)
                player.inventory.items[item] -= 1
            elif item == "red_potion":
                text, player.hp = heal(player.name, player.hp, player.hpmax, 25)
                player.inventory.items[item] -= 1
            elif item == "litle_red_potion":
                text, player.hp = heal(player.name, player.hp, player.hpmax, 10)
                player.inventory.items[item] -= 1

            return text, object_used
        else:
            return "You can't use this item.", object_used
    else:
        return "You have no more " + item.replace("_", " ").title() + ".", object_used


# Use boat.
def use_boat(x: int, y: int, player: Player(), set_map: dict) -> tuple[str, dict]:
    if "boat" in set_map[str((x, y))]["items"] and player.status != 1:
        player.status = 1
        set_map[str((x, y))]["items"].remove("boat")
        if str((x, y)) == "(6, 2)":
            set_map[str((x, y))]["d"] = "Seaside with swaying palm trees, echoing waves, and vibrant life. A " \
                                        "solitary figure stands at the water's edge, gazing out into the " \
                                        "vastness of the sea, captivated by the rhythmic dance of the waves and " \
                                        "the boundless horizon stretching before them."
        else:
            set_map[str((x, y))]["d"] = "Seaside with swaying palm trees, echoing waves, and vibrant life."
        return "You are in the boat.", set_map
    elif player.status == 1:
        return "You are already in the boat.", set_map
    else:
        return "There is no boat here.", set_map


# Wait action.
def wait(actual_hs, opt: str) -> tuple[str, int, str]:
    if opt not in ["morning", "afternoon", "evening", "night"]:
        hs, d_moment = day_est(actual_hs, 0)
        return "This is not posible.", actual_hs, d_moment
    elif opt == "morning":
        return "You wait until the morning.", 6, "MORNING"
    elif opt == "afternoon":
        return "You wait until the afternoon.", 12, "AFTERNOON"
    elif opt == "evening":
        return "You wait until the evening.", 18, "EVENING"
    else:
        return "You slept wait the night.", 22, "NIGHT"
