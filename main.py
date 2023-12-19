# Imports.
# External imports.
import os
import random
import numpy as np
import matplotlib.pyplot as plt

# Locals imports.
from actions import move, equip, use_boat, land, sleep_in_bed, wait, talk, enter, explore, battle, heal, unequip, drop, \
    event_handler, use, check
from displays import disp_play, disp_sleep, disp_talk, disp_title, disp_wait, disp_enter, disp_assign, disp_equip,\
    disp_show_inventory, disp_drop, disp_look_around
import globals
from utils import label_pixels, draw_move, tl_map_set, day_est, export_dict_to_txt, load_dict_from_txt, clear, \
    check_name, get_hash, sum_item_stats
from management import save


# Command line settings.
os.system(f"mode con: cols={globals.WIDTH} lines={globals.HEIGHT}")

# Game variables.
run = True
menu = True
play = False
rules = False

# Play variables.
fight = False
standing = True
day_time = 6
day_moment = "MORNING"
add_hs = 0

# Player variables.
user_stats = {
    "name": "",
    "hp": 25,
    "hpmax": 25,
    "lvl": 1,
    "exp": 0,
    "expmax": 10,
    "atk": 0,
    "def": 0,
    "eva": 0,
    "pre": 0,
    "b_hpmax": 25,
    "b_atk": 2,
    "b_def": 1,
    "b_eva": 0,
    "b_pre": 0.7,
    "b_str": 0,
    "b_agi": 0,
    "b_vit": 0,
    "b_res": 0,
    "b_dex": 0,
    "x": 0,
    "y": 0,
    "x_cp": 0,
    "y_cp": 0,
    "hability_points": 0,
    "slot1": "Red Potion",
    "slot2": "Litle Red Potion"
}

user_equip = {
    "head": None,
    "chest": None,
    "right_hand": None,
    "left_hand": None,
    "legs": None,
}

x = user_stats["x"]
y = user_stats["y"]

# Player map.
user_map = np.zeros((32, 32, 4), dtype=np.uint8)
user_map[:, :, 3] = np.ones((32, 32), dtype=np.uint8) * 255

# Inventory.
inventory = {}

# Global settings.
tile_map = label_pixels("rsc.png")
map_set = tl_map_set(tile_map)
y_len = len(tile_map)-1
x_len = len(tile_map[0])-1

bioms = globals.BIOMS.copy()
npc = globals.NPC.copy()
mobs = globals.MOBS.copy()

screen = "Nothing done yet."


# Main loop of the game.
while run:
    # Menu loop.
    while menu:
        clear()
        disp_title()

        print(" < MENU >")
        print()
        print(" 1 - NEW GAME")
        print(" 2 - LOAD GAME")
        print(" 3 - RULES")
        print(" 4 - QUIT GAME")
        print()

        # Rules.
        if rules:
            clear()
            disp_title()

            print()
            print()
            print(" < RULES >")
            print()
            print(" I'm the creator of this game and these are the rules.")
            print()
            print(" 1) Follow your path.")
            print(" 2) Trace your path with: 'map' and 'draw map'.")
            print(" 3) Many action are allowed ('use', 'enter', 'talk', 'explore', etc.) try them "
                  "\n    to find your path.")
            print(" 4) Remember: sleeping ('sleep to') in a bed, will charge your energy.")
            print()
            rules = False
            choice = ""
            input(" > ")
        else:
            choice = input(" # ")

        # New game choice.
        if choice == "1":
            clear()
            try:
                load_setting = load_dict_from_txt("cfg_save.txt")
                L_NAME = load_setting["1"]["name"]
                L_HP = int(load_setting["1"]["hp"])
                L_HPMAX = int(load_setting["1"]["hpmax"])
                L_LVL = int(load_setting["1"]["lvl"])
                L_EXP = int(load_setting["1"]["exp"])
                L_EXPMAX = int(load_setting["1"]["expmax"])

                disp_title()

                print(" < NEW GAME >")
                print()
                print(" There is already a game existing, do you want to delete it?")
                print()
                print(" NAME: " + str(L_NAME) + " / LVL: " + str(L_LVL))
                print()
                print(" 1 - Yes")
                print(" 2 - No")
                print()
                action_choice = input(" # ")

                if action_choice == "2":
                    pass
                elif action_choice == "1":
                    # Play variables.
                    fight = False
                    standing = True
                    day_time = 6
                    day_moment = "MORNING"
                    add_hs = 0

                    # Player variables.
                    user_stats = {
                        "name": "",
                        "hp": 25,
                        "hpmax": 25,
                        "lvl": 1,
                        "exp": 0,
                        "expmax": 10,
                        "atk": 0,
                        "def": 0,
                        "eva": 0,
                        "pre": 0,
                        "b_hpmax": 25,
                        "b_atk": 2,
                        "b_def": 1,
                        "b_eva": 0,
                        "b_pre": 0.7,
                        "b_str": 0,
                        "b_agi": 0,
                        "b_vit": 0,
                        "b_res": 0,
                        "b_dex": 0,
                        "x": 0,
                        "y": 0,
                        "x_cp": 0,
                        "y_cp": 0,
                        "hability_points": 0,
                        "slot1": "Red Potion",
                        "slot2": "Litle Red Potion"
                    }

                    user_equip = {
                        "head": None,
                        "chest": None,
                        "right_hand": None,
                        "left_hand": None,
                        "legs": None,
                    }

                    x = user_stats["x"]
                    y = user_stats["y"]

                    # Player map.
                    user_map = np.zeros((32, 32, 4), dtype=np.uint8)
                    user_map[:, :, 3] = np.ones((32, 32), dtype=np.uint8) * 255

                    # Inventory.
                    inventory = {}

                    # Global settings.
                    tile_map = label_pixels("world_map.png")
                    map_set = tl_map_set(tile_map)
                    y_len = len(tile_map) - 1
                    x_len = len(tile_map[0]) - 1

                    bioms = globals.BIOMS.copy()
                    npc = globals.NPC.copy()
                    mobs = globals.MOBS.copy()

                    screen = "Nothing done yet."
                    
                    user_stats["name"] = ""
                    while not check_name(user_stats["name"]):
                        user_stats["name"] = input(" # What's your NAME, hero? ").title()
                    menu = False
                    play = True

            except:
                clear()
                disp_title()

                print(" < NEW GAME >")
                print()

                user_stats["name"] = ""
                while not check_name(user_stats["name"]):
                    user_stats["name"] = input(" # What's your NAME, hero? ").title()
                menu = False
                play = True

            # Initial settings.
            # Inventory variables.
            inventory = {"walk": True, "message": False, "red_potion": 1, "litle_red_potion": 2, "gold": 5}
            # Map settings.
            map_set.update(globals.MAP_SETTING)
            # Location setting.
            map_set[str((x, y))]["t"] = user_stats["name"] + "'s Hut"
            # Introduction setting.
            npc["whispers"][0] = [user_stats["name"] + "...", user_stats["name"] + "...", "...your destiny awaits.",
                                  "Follow the whispers of the wind, and come to me.", "Secrets untold and challenges "
                                  "unknown lie ahead.", "Trust in the unseen path...", "... come to me."]

            # Introduction.
            if user_stats["name"]:
                screen, inventory = talk(npc=npc["whispers"], npc_name="Whispers", inventory=inventory)

            # Dragon Firefrost setting.
            npc["dragon firefrost"][0] = [user_stats["name"] + "...", "You finally come to me...", "Destiny calls "
                                         "for a dance of fire and frost between us...", "Ready your blade..."]

        elif choice == "2":  # Load game choice.
            try:
                clear()
                disp_title()
                print(" < LOAD GAME >")
                print()

                # Loading user map.
                map_load = np.loadtxt("cfg_map.txt", delimiter='\t', dtype=int)
                user_map = map_load.reshape((32, 32, 4))

                # Loading inventory, user stats and map settings.
                load_setting = load_dict_from_txt("cfg_save.txt")
                load_hash = load_dict_from_txt("cfg_hash.txt")
                if get_hash("cfg_save.txt") != load_hash["hash"]:
                    raise OSError

                inventory.update(load_setting["0"])
                user_stats.update(load_setting["1"])
                npc.update(load_setting["2"])
                user_equip.update(load_setting["3"])
                map_set.update(load_setting["9"])

                x = user_stats["x"]
                y = user_stats["y"]

                menu = False
                play = True

                print(" Welcome back " + user_stats["name"] + ".")
                input(" > ")

            except OSError:
                print(" No loadable save file or corrupt file.")
                play = False
                print()
                input(" > ")

        elif choice == "3":  # Show rules option.
            rules = True

        elif choice == "4":  # Quit option.
            quit()

    while play:
        save(user_stats, user_equip, user_map, inventory, npc, map_set, x, y)  # Autosave.
        clear()

        # Fight chances of moving.
        if not standing:
            if map_set[str((x, y))]["e"]:
                if random.randint(0, 100) < max(bioms[tile_map[y][x]]["e_chance"]):
                    enemy = random.choices(bioms[tile_map[y][x]]["e_list"], bioms[tile_map[y][x]]["e_chance"], k=1)[0]
                    user_stats, inventory, play, menu, win = battle(user_stats, mobs[enemy].copy(), inventory, map_set)
                    save(user_stats, user_equip, user_map, inventory, npc, map_set, x, y)

        # Lvl upgrade of user.
        if user_stats["exp"] >= user_stats["expmax"]:
            user_stats["lvl"] += 1
            user_stats["exp"] = 0
            user_stats["expmax"] = 10 * user_stats["lvl"]
            user_stats["b_hpmax"] += 2
            user_stats["b_atk"] += 0.4
            user_stats["b_def"] += 0.025
            user_stats["b_pre"] += 0.005
            user_stats["b_eva"] += 0.01
            screen = "You have lvl up. ASSIGN Strength/Agility/Vitality. You can assign 3 points."
            user_stats["hability_points"] += 3

        # Refreshing stats of user.
        items_stats = sum_item_stats(user_equip)
        user_stats["hpmax"] = user_stats["b_hpmax"] + user_stats["b_vit"] * 2
        user_stats["atk"] = user_stats["b_atk"] + int(user_stats["b_str"] * 0.4) + items_stats["atk"]
        user_stats["def"] = user_stats["b_def"] + int(user_stats["b_res"] * 0.4) + items_stats["def"]
        user_stats["eva"] = user_stats["b_eva"] + user_stats["b_agi"] * 0.01 + items_stats["eva"]
        user_stats["pre"] = user_stats["b_pre"] + user_stats["b_agi"] * 0.005 + items_stats["pre"]

        if play:
            # Setting enviroment variables.
            location = map_set[str((x, y))]["t"] if map_set[str((x, y))]["t"] else bioms[tile_map[y][x]]["t"]
            # Location description setting.
            if map_set[str((x, y))]["d"]:
                loc_des = map_set[str((x, y))]["d"]
            else:
                loc_des = bioms[tile_map[y][x]]["d"]

            # Day time and day moment.
            day_time, day_moment = day_est(day_time, add_hs)
            add_hs = 0

            # Draw of general stats.
            clear()
            disp_play(user_stats, inventory, location, "NAIWAT", day_moment, loc_des, inventory["red_potion"], "Empty",
                      x, y, draw_move(x, y, x_len, y_len, inventory, tile_map, map_set),
                      [user_stats["slot1"], user_stats["slot2"]], screen, 36)

            # Input action.
            print()
            action = input(" " * 2 + "# ").lower().split()
            if not action:
                action = ["None"]

            # Action ejecution.
            if action[0] == "0":  # Save game.
                play = False
                menu = True
                save(user_stats, user_equip, user_map, inventory, npc, map_set, x, y)

            if action[0] in ["1", "2", "3", "4"]:  # Move action.
                screen, x, y, add_hs, standing = move(x, y, x_len, y_len, inventory, tile_map, action[0], map_set)

            elif action[0] in ["5", "6"]:  # Use object action.
                if action[0] == "5":
                    fast_object = user_stats["slot1"]
                if action[0] == "6":
                    fast_object = user_stats["slot2"]
                screen, user_stats, inventory, object_used = use(user_stats, inventory, fast_object)
                standing = True

            elif action[0] == "assign":  # Assign action.
                if len(action) < 2:
                    screen = disp_assign(user_stats)
                elif user_stats["hability_points"]:
                    if action[1] in ["strength", "str"]:
                        user_stats["b_str"] += 1
                        user_stats["hability_points"] -= 1
                        screen = "You have assigned a skill point to strength."
                    elif action[1] in ["agility", "agi"]:
                        user_stats["b_agi"] += 1
                        user_stats["hability_points"] -= 1
                        screen = "You have assigned a skill point to agility."
                    elif action[1] in ["resistance", "res"]:
                        user_stats["b_res"] += 1
                        user_stats["hability_points"] -= 1
                        screen = "You have assigned a skill point to resistance."
                    # elif action[1] in ["dexterity", "dex"]:
                    #     user_stats["b_dex"] += 1
                    #     user_stats["hability_points"] -= 1
                    #     screen = "You have assigned a skill point to dexterity."
                    elif action[1] in ["vitality", "vit"]:
                        user_stats["b_vit"] += 1
                        user_stats["hability_points"] -= 1
                        screen = "You have assigned a skill point to vitality."
                elif user_stats["hability_points"] == 0:
                    screen = "You have no more skill points left."
                else:
                    "That is not posible."
                standing = True

            elif action[0] == "check":  # Check action.
                screen = check(x, y, map_set, " ".join(action[1:]))

            elif action == ["draw", "map"]:  # Update of map action.
                user_map[y][x] = bioms[tile_map[y][x]]["c"]
                if x != 0:
                    user_map[y][x - 1] = bioms[tile_map[y][x - 1]]["c"]
                if x != x_len:
                    user_map[y][x + 1] = bioms[tile_map[y][x + 1]]["c"]
                if y != 0:
                    user_map[y - 1][x] = bioms[tile_map[y - 1][x]]["c"]
                if y != y_len:
                    user_map[y + 1][x] = bioms[tile_map[y + 1][x]]["c"]
                screen = "You have explored the area and mapped it out."

                if "telescope" in inventory.keys():
                    # Explore a square instead of a cross
                    for i in range(max(0, x - 1), min(x_len, x + 2)):
                        for j in range(max(0, y - 1), min(y_len, y + 2)):
                            user_map[j][i] = bioms[tile_map[j][i]]["c"]

            elif action[0] == "drop":  # Drop action.
                if len(action) <= 2:
                    screen = disp_drop()
                    standing = True
                else:
                    screen, inventory = drop(inventory, " ".join(action[2:]), int(action[1]))

            elif action[0] == "enter":  # Enter action.
                if len(action) <= 2:
                    screen = disp_enter(x, y, map_set)
                    standing = True
                elif " ".join(action[2:]) in map_set[str((x, y))]["entries"]:
                    screen, x, y, fight = enter(x, y, " ".join(action[2:]), inventory)
                    if fight:
                        user_stats, inventory, play, menu, win = battle(user_stats, mobs["orc"].copy(), inventory, map_set)
                        if not play:
                            save(user_stats, user_equip, user_map, inventory, npc, map_set, x, y)
                    standing = True
                else:
                    screen = "There is no " + " ".join(action[2:]) + "."
                    standing = True

            elif action[0] in ["equip"] or action == ["show", "equip"]:  # Equip action.
                if len(action) <= 1:
                    screen = disp_equip(user_equip)
                    standing = True
                else:
                    screen, user_equip, inventory = equip(inventory, user_equip, " ".join(action[1:]))
                    standing = True

            elif action[0] == "explore":  # Explore action:
                screen, map_set = explore(x, y, map_set)
                standing = False

            elif action[0] == "land":  # Land action.
                screen, inventory, map_set = land(x, y, inventory, map_set, tile_map)
                standing = False

            elif action[0] == "listen":  # Listen action.
                screen = "You don't hear anything special."

            elif action == ["look", "around"]:  # Look around action.
                screen = disp_look_around(user_stats, map_set)

            elif action[0] in ["map"] or action == ["show", "map"]:  # Show map.
                user_map[y][x] = globals.PINK
                plt.figure(user_stats["name"] + "'s map")
                plt.imshow(user_map)
                plt.title("Map")
                plt.show()
                user_map[y][x] = globals.BIOMS[tile_map[y][x]]["c"]
                standing = True

            elif action[0] == "slot1":  # Selection slot1 action.
                item_select = "_".join(action[1:])
                if item_select in globals.ITEMS_SELL and item_select in inventory.keys():
                    user_stats["slot1"] = " ".join(action[1:]).title()

            elif action[0] == "slot2":  # Selection slot1 action.
                item_select = "_".join(action[1:])
                if item_select in globals.ITEMS_SELL and item_select in inventory.keys():
                    user_stats["slot2"] = " ".join(action[1:]).title()

            elif action == ["show", "inventory"] or action[0] in ["inventory", "inv"]:
                screen = disp_show_inventory(inventory)
                standing = True

            elif action[0] == "sleep":  # Sleep action.
                if len(action) <= 2:
                    screen = disp_sleep(x, y, map_set)
                    standing = True
                else:
                    screen, user_stats["hp"], day_time, day_moment = sleep_in_bed(x, y, map_set, user_stats["hp"], user_stats["hpmax"], day_time, action[2])
                    user_stats["x_cp"], user_stats["y_cp"] = x, y
                    standing = True

            elif action[0] == "talk":  # Talk action.
                npc_name = " ".join(action[2:]).lower()
                if len(action) <= 2:
                    screen = disp_talk(x, y, map_set)
                    standing = True
                elif npc_name in map_set[str((x, y))]["npc"]:
                    screen, inventory = talk(npc=npc[npc_name], npc_name=npc_name, inventory=inventory)
                    standing = True
                else:
                    screen = "Here no one is called " + npc_name.title() + "."
                    standing = True

            elif action == ["use", "boat"]:  # Use boat action.
                screen, inventory, map_set = use_boat(x, y, inventory, map_set)
                standing = True

            elif action[0] == "unequip":  # Unequip action.
                if len(action) <= 1:
                    screen = disp_equip(user_equip)
                    standing = True
                else:
                    screen, user_equip, inventory = unequip(inventory, user_equip, " ".join(action[1:]))
                    standing = True

            elif action[0] == "wait":  # Wait action.
                if len(action) <= 2:
                    screen = disp_wait()
                    standing = True
                else:
                    screen, day_time, day_moment = wait(day_time, action[2])
                    standing = False

            elif action[0] == "update":  # Admin action for update de game while devolping.
                inventory["scales"] = 4121996
                screen = "Map updated."
            else:
                standing = True

            # Event handler.
            user_stats, inventory, npc, map_set, play, menu = event_handler(user_stats, user_equip, user_map, inventory,
                                                                            npc, map_set, mobs, x, y, play, menu)
