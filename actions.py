# Imports.
import globals
from utils import day_est, typewriter, clear, text_ljust, coast_reset
from displays import disp_battle, disp_talk, disp_talk_util, disp_title
import random


# Battle action.
def battle(user: dict, enemy: dict, inventory: dict, ms: dict):

    screen = "Defeat de enemy!"
    play = True
    menu = False
    fight = True

    while fight:
        disp_battle(user, enemy, screen, inventory)
        choice_action = input(" # ")  # User choice action.
        screen = "."  # Clearing text output screen.

        if choice_action == "1":  # Attack option.
            if user["pre"] * (1 - enemy["eva"]) > random.random():
                USER_DMG = max(int(int(user["atk"]) - int(enemy["def"])), 0)
                enemy["hp"] -= USER_DMG
                screen = " " + user["name"] + " dealt " + str(USER_DMG) + " damage to the " + enemy["name"] + "."
            else:
                screen = " " + user["name"] + " fail the attack."

        elif choice_action in ["2", "3"]:  # Use object action.
            if choice_action == "2":
                fast_object = user["slot1"]
            if choice_action == "3":
                fast_object = user["slot2"]
            screen, user_stats, inventory = use(user, inventory, fast_object)

        # Enemy attack.
        if enemy["hp"] > 0 and choice_action in ["1", "2", "3"]:
            if enemy["pre"] * (1 - user["eva"]) > random.random():
                ENEMY_ATK = [[enemy["atk"], enemy["atk"] * 1.7], [80, 20]]
                ENEMY_DMG = max(int(int(random.choices(ENEMY_ATK[0], ENEMY_ATK[1], k=1)[0]) - int(user["def"])), 0)
                user["hp"] -= ENEMY_DMG
                screen += "\n " + enemy["name"] + " dealt " + str(ENEMY_DMG) + " damage to " + user["name"] + "."
            else:
                screen += "\n " + enemy["name"] + " fail the attack."
        input(" > ")

        # Logic of fight status or result.
        if user["hp"] <= 0:
            disp_battle(user, enemy, screen, inventory)
            screen += "\n " + enemy["name"] + " defeated " + user["name"] + "..."
            disp_battle(user, enemy, screen, inventory)
            input(" > ")
            play = False
            menu = True
            user["hp"], user["x"], user["y"] = int(user["hpmax"]), user["x_cp"], user["y_cp"]
            inventory["walk"] = True
            user["exp"] = 0
            try:
                del inventory["boat"]
            except KeyError:
                pass
            coast_reset(ms=ms, keys=["(2, 1)", "(6, 2)"])
            print(" GAME OVER")
            input(" > ")
            return user, inventory, play, menu, 0

        if enemy["hp"] <= 0:
            screen += "\n " + "You defeated the " + enemy["name"] + "!"
            fight = False

            # Drop items logic.
            user["exp"] += enemy["exp"]
            if enemy["items"]:
                drop_quantity = random.randint(1, len(enemy["items"])) - 1
                drop = list(set(random.choices([*enemy["items"].keys()], cum_weights=enemy["dc_items"], k=drop_quantity)))

                for item in drop:
                    if item != "none" and item in inventory.keys():
                        inventory[item] += enemy["items"][item]
                        screen += "\n You've found " + str(enemy["items"][item]) + " " + item.replace("_", " ").title() + "."
                    elif item != "none":
                        inventory[item] = enemy["items"][item]

            screen += "\n You have gained " + str(enemy["exp"]) + " experience."

    disp_battle(user, enemy, screen, inventory)
    input(" > ")
    return user, inventory, play, menu, 1


# Buy action.
def buy(inv: dict, item: str, quantity: int, price: int) -> tuple[str, dict]:
    if inv["gold"] >= price:
        try:
            inv[item] += quantity
        except KeyError:
            inv[item] = quantity
        inv["gold"] -= price * quantity
        return "You buy " + str(quantity) + " " + item.replace("_", " ").title() + ".", inv
    else:
        return "You don't have enough gold.", inv


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
def drop(inv: dict, item_name: str, quantity: int = 1) -> tuple[str, dict]:
    item = item_name.replace(" ", "_")
    try:
        if inv[item] >= int(quantity) and item not in ["red_potion", "walk"]:
            inv[item] -= int(quantity)
            if inv[item] <= 0:
                del inv[item]
            return "You drop " + str(quantity) + " " + item_name.title() + ".", inv
        else:
            return "You don't have " + str(quantity) + " " + item_name.title() + ".", inv
    except KeyError:
        return "You don't have " + item_name.title() + ".", inv


# Enter action.
def enter(x: int, y: int, entrie: str, inv: dict) -> tuple[str, int, int, bool]:
    if entrie == "castle":
        return "You cannot enter here.", x, y, False

    if entrie == "cathedral":
        return "You cannot enter here.", x, y, False

    elif entrie == "cave":
        if (x, y) == (13, 0):
            if "torch" in inv.keys():
                if random.randint(0, 100) <= 10:
                    return "You have crossed the cave without any problems.", 19, 0, False
                else:
                    return "You have crossed the cave.", 19, 0, True
            else:
                return "You need a torch to enter.", x, y, False

        if (x, y) == (19, 0):
            if "torch" in inv.keys():
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
def equip(inv: dict, equiped: dict, item_name: str) -> tuple[str, dict, dict]:
    item = item_name.replace(" ", "_").lower()
    if item in inv.keys() and item in globals.ITEMS_EQUIP.keys():
        body_part = globals.ITEMS_EQUIP[item]["body"]
        if not equiped[body_part]:
            equiped[body_part] = item
            inv[item] -= 1
            return "You have equip " + item_name.title() + ".", equiped, inv
        else:
            return "You already have an item equipped. UNEQUIP " + equiped[body_part].title() + ".", equiped, inv
    elif item not in inv.keys():
        return "You don't have " + item_name.title() + ".", equiped, inv
    elif item not in globals.ITEMS_EQUIP.keys():
        return "You can't equip " + item_name.title() + ".", equiped, inv


# Event handler.
def event_handler(user: dict, inv: dict, npc: dict, action: list, ms: dict, mobs: dict, play: int, menu: int) -> tuple[dict, dict, dict, dict, int, int]:
    if npc["fisherman marlin"][3][0] and not npc["guard lorian"][3][1]:
        npc["guard lorian"] = [["Halt, traveler! Hyrule City permits only those with proper credentials to pass these "
                                "gates.", "State your business and present your identification, or you shall not "
                                "venture beyond.", "The safety of our citizens is paramount, and we cannot afford to be "
                                "lax in these trying times."],
                               [["I have a message", ["Marlin, you say?", "Well, that old "
                                "sea dog never forgets his family. Very well, you may pass. Tell him to visit when his "
                                "fishing tales become too much for the villagers.", "Safe travels, adventurer."]],
                                ["Leave", ["..."]]],
                               [], [0, 0, 0]]

        return user, inv, npc, ms, play, menu

    elif npc["guard lorian"][3][1] and not inv["message"]:
        npc["guard lorian"] = [["You've gained entry, but heed this counsel: Beyond the western outskirts lies "
                                "uncharted territories and lurking dangers.", "Arm yourself well, noble traveler. The "
                                "path is treacherous, and a sturdy sword or enchanted bow may be your greatest allies.",
                                "Antina City rests in relative peace, but the world beyond is unpredictable. "
                                "Safe travels, and may your blade remain sharp against the shadows that may encroach "
                                "upon your journey."], [], [], [0, True, 0]]
        inv["message"] = True
        inv["permission"] = True

        return user, inv, npc, ms, play, menu

    elif npc["dragon firefrost"][3][0]:
        user, inv, play, menu, win = battle(user, mobs["dragon"].copy(), inv, ms)
        if win:
            npc["dragon firefrost"] = [["Impressive. Today, the winds of fate favor you.", "I yield. But heed my words,"
                                        " for when the stars align in a different cosmic dance, I shall await you "
                                        "once more.", "Until then, let the echoes of our encounter linger in the "
                                        "mountain breeze. Farewell, Elina.", "Until our destinies entwine again."],
                                       [], [], [0]]
            screen, inv = talk(npc=npc["dragon firefrost"], npc_name="dragon firefrost", inventory=inv)
            ms["(11, 24)"]["npc"] = []
            ms["(0, 0)"]["items"].append("origami flowers")
            npc["dragon firefrost"] = [[], [], [], [0]]
        return user, inv, npc, ms, play, menu

    else:
        return user, inv, npc, ms, play, menu


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
def land(x: int, y: int, inventory: dict, set_map: dict, tl_map: list) -> tuple[str, dict, dict]:
    if "boat" in inventory.keys() and tl_map[y][x] not in ["sea", "river"]:
        inventory["walk"] = True
        del inventory["boat"]
        set_map[str((x, y))]["items"].append("boat")
        try:
            set_map[str((x, y))]["d"] = globals.MAP_SETTING[str((x, y))]["d"]
        except KeyError:
            set_map[str((x, y))]["d"] = "Seaside with anchored boat, echoing waves and vibrant coastal life."
        return "You have land.", inventory, set_map
    else:
        if "boat" in inventory.keys():
            return "You can't land here.", inventory, set_map
        else:
            return "You aren't in a boat.", inventory, set_map


# Move function.
def move(
        x: int, y: int, map_heigt: int, map_width: int, inventory: dict,
        tl_map: list, mv: str, ms: dict) -> tuple[str, int, int, int]:
    hs = 8
    # Move North.
    if y > 0 and all(req in [*inventory.keys()] for req in ms[str((x, y - 1))]["r"]) and mv == "1":
        if (tl_map[y - 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y - 1][x] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y - 1][x] in ["town", "gates"]):
            return "You moved North.", x, y - 1, hs
    # Move East.
    if x < map_heigt and all(req in [*inventory.keys()] for req in ms[str((x + 1, y))]["r"]) and mv == "2":
        if (tl_map[y][x + 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y][x + 1] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y][x + 1] in ["town", "gates"]):
            return "You moved East.", x + 1, y, hs

    # Move South.
    if y < map_width and all(req in [*inventory.keys()] for req in ms[str((x, y + 1))]["r"]) and mv == "3":
        if (tl_map[y + 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y + 1][x] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y + 1][x] in ["town", "gates"]):
            return "You moved South.", x, y + 1, hs

    # Move West.
    if x > 0 and all(req in [*inventory.keys()] for req in ms[str((x - 1, y))]["r"]) and mv == "4":
        if (tl_map[y][x - 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y][x - 1] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y][x - 1] in ["town", "gates"]):
            return "You moved West.", x - 1, y, hs
    return "You can't move there.", x, y, hs


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
def sell(inv: dict, item: str, quantity: int, price: int) -> tuple[str, dict]:
    try:
        if inv[item] >= quantity:
            inv[item] -= quantity
            inv["gold"] += quantity * price
            return "You sell " + str(quantity) + " " + item.replace("_", " ").title() + ". You earn " + str(quantity * price) + " gold.", inv
        else:
            return "You don't have enough " + item.replace("_", " ").title() + ".", inv
    except KeyError:
        return "You don't have enough " + item.replace("_", " ").title() + ".", inv


# Talk.
def talk(npc: dict, npc_name: str, inventory: dict = None) -> tuple[str, dict]:
    clear()
    for line in npc[0]:
        disp_talk_util(npc_name)
        lines = text_ljust(line, width=70)
        for text in lines:
            typewriter(" " * 4 + text)
            print()

        input(" " * 4 + "> ")
    npc[3][0] = True  # Turning True first message of NPC.

    if npc[1]:
        print()
        for i, res in enumerate(npc[1]):
            print(" " * 4 + str(i + 1), ") " + res[0].capitalize() + ".")
        print()

        while True:
            try:
                action_choice = int(input(" " * 4 + "# ")) - 1
                if 0 <= action_choice <= len(npc[1]):
                    npc[3][action_choice + 1] = True  # Turning True response message of NPC.
                    break
            except ValueError:
                pass

        for line in npc[1][action_choice][1]:
            disp_talk_util(npc_name)
            lines = text_ljust(line, width=70)
            for text in lines:
                typewriter(" " * 4 + text)
                print()

            input(" " * 4 + "> ")

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
                print(" " * 6 + "[GOLD: " + str(inventory["gold"]) + "]\n")
                
                while True:
                    try:
                        item = int(input(" " * 4 + "# ")) - 1
                        if 0 <= item < len(items):
                            if item == len(items) - 1:  # Quit condition.
                                return "Nothing done.", inventory
                            print()
                            print(" " * 4 + "How many " + items[item].replace("_", " ").title() + " do you want to buy?")
                            while True:
                                try:
                                    quantity = int(input(" " * 4 + "# "))
                                    return buy(inventory, items[item], quantity, prices[item])
                                except ValueError:
                                    pass
                        else:
                            return "Nothing done.", inventory
                    except ValueError:
                        pass

            elif npc[1][action_choice][0] == "sell":
                print()
                items = []
                prices = []
                n = 0
                for item, value in {key: globals.ITEMS_SELL[key] for key in set(inventory.keys()).intersection(set(globals.ITEMS_SELL.keys())) if inventory[key] > 0}.items():
                    if item != "quit":
                        line_text = text_ljust(str(n + 1) + ") " + item.replace("_", " ").title() + " x " + str(value) + " gold.", 30)
                        print(" " * 6 + line_text[0] + "[" + str(inventory[item]) + "]")
                    else:
                        print(" " * 6 + str(n + 1) + ") " + item.replace("_", " "))
                    items.append(item)
                    prices.append(value)
                    n += 1
                print(" " * 6 + str(n + 1) + ") Quit.")
                items.append("quit")
                print()
                print(" " * 6 + "GOLD: " + str(inventory["gold"]) + ".\n")

                while True:
                    try:
                        item = int(input(" " * 4 + "# ")) - 1
                        if item == len(items) - 1:  # Quit condition.
                            return "Nothing done.", inventory
                        if 0 <= item < len(items):
                            print()
                            print(" " * 4 + "How many " + items[item].replace("_", " ").title() + " do you want to sell?")
                            while True:
                                try:
                                    quantity = int(input(" " * 4 + "# "))
                                    return sell(inventory, items[item], quantity, prices[item])
                                except ValueError:
                                    pass
                        else:
                            return "Nothing done.", inventory
                    except ValueError:
                        pass

            else:
                return ".", inventory

        else:
            return ".", inventory

    else:
        return ".", inventory


# Unequip action.
def unequip(inv: dict, equiped: dict, item_name: str) -> tuple[str, dict, dict]:
    item = item_name.replace(" ", "_").lower()
    if item in equiped.values():
        body_part = globals.ITEMS_EQUIP[item]["body"]
        equiped[body_part] = None
        try:
            inv[item] += 1
            return "You have unequip " + item_name.title() + ".", equiped, inv
        except KeyError:
            inv[item] = 1
            return "You have unequip " + item_name.title() + ".", equiped, inv
    else:
        return "You don't have " + item_name.title() + " equipped.", equiped, inv


# Use action (general).
def use(user: dict, inv: dict, obj: str):
    item = obj.replace(" ", "_").lower()
    if inv[item] > 0:
        if "potion" in item:
            if item == "giant_red_potion":
                text, user["hp"] = heal(user["name"], user["hp"], user["hpmax"], 40)
                inv[item] -= 1
            elif item == "red_potion":
                text, user["hp"] = heal(user["name"], user["hp"], user["hpmax"], 25)
                inv[item] -= 1
            elif item == "litle_red_potion":
                text, user["hp"] = heal(user["name"], user["hp"], user["hpmax"], 10)
                inv[item] -= 1

            return text, user, inv
        else:
            return "You can't use this item.", user, inv
    else:
        return "You have no more " + item.replace("_", " ").title() + ".", user, inv


# Use boat.
def use_boat(x: int, y: int, inventory: dict, set_map: dict) -> tuple[str, dict, dict]:
    if "boat" in set_map[str((x, y))]["items"] and "boat" not in inventory.keys():
        inventory["boat"] = True
        del inventory["walk"]
        set_map[str((x, y))]["items"].remove("boat")
        if str((x, y)) == "(6, 2)":
            set_map[str((x, y))]["d"] = "Seaside with swaying palm trees, echoing waves, and vibrant life. A " \
                                        "solitary figure stands at the water's edge, gazing out into the " \
                                        "vastness of the sea, captivated by the rhythmic dance of the waves and " \
                                        "the boundless horizon stretching before them."
        else:
            set_map[str((x, y))]["d"] = "Seaside with swaying palm trees, echoing waves, and vibrant life."
        return "You are in the boat.", inventory, set_map
    elif "boat" in inventory.keys():
        return "You are already in the boat.", inventory, set_map
    else:
        return "There is no boat here.", inventory, set_map


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
