# Imports.
# External imports.
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Locals imports.
from actions import drop, enter, equip, explore, leave, land, move, sleep_in_bed, wait, talk, battle, pick_up,\
    unequip, use, use_boat, check
from biome import Entry
from displays import disp_play, disp_sleep, disp_talk, disp_title, disp_wait, disp_enter, disp_assign, disp_equip,\
    disp_show_inventory, disp_drop, disp_look_around
import globals
from management import event_handler, init_map_setting, save
from player import Player
from utils import coordstr, import_player, import_settings, label_pixels, load_map_set, draw_move, tl_map_set, day_est,\
    load_dict_from_txt, clear, check_name, get_hash, sum_item_stats, export_dict_to_txt

# Game variables.
run = True
menu = True
play = False
rules = False

# Play variables.
fight = False
standing = True
year = 96
day_time = 6
day_moment = "MORNING"
add_hs = 0

# Player variables.
player = Player()

x = player.x  # X location.
y = player.y  # Y location.

inventory = player.inventory  # Inventory.

# Global settings.
tile_map = label_pixels("rsc/tile-00.png")
map_set = tl_map_set(tile_map)
y_len = len(tile_map)-1
x_len = len(tile_map[0])-1

npc = globals.NPCS.copy()
mobs = globals.MOBS.copy()

screen = random.choices(population=["Nothing done yet.", "Waiting for commands."], weights=[50, 50], k=1)[0]


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
                load_setting = import_player("cfg_save.pkl")
                L_NAME = load_setting.name
                L_HP = load_setting.hp
                L_HPMAX = load_setting.hpmax
                L_LVL = load_setting.lvl
                L_EXP = load_setting.exp
                L_EXPMAX = load_setting.expmax

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
                    player = Player()

                    x = player.x  # X location.
                    y = player.y  # Y location.

                    inventory = player.inventory  # Inventory.

                    # Global settings.
                    tile_map = label_pixels("rsc.png")
                    map_set = tl_map_set(tile_map)
                    y_len = len(tile_map) - 1
                    x_len = len(tile_map[0]) - 1

                    npc = globals.NPCS.copy()
                    mobs = globals.MOBS.copy()

                    screen = "Nothing done yet."

                    while not check_name(player.name):
                        player.name = input(" # What's your NAME, hero? ").title()
                    menu = False
                    play = True

            except:
                clear()
                disp_title()

                print(" < NEW GAME >")
                print()

                while not check_name(player.name):
                    player.name = input(" # What's your NAME, hero? ").title()
                menu = False
                play = True

            # Initial settings.
            # Map settings.
            init_map_setting(map_set)

            # Location setting.
            map_set[coordstr(0, 0)].entries["hut"].name = player.name + "'s Hut"
            player.place = map_set[coordstr(0, 0)].entries["hut"]

            # Introduction setting.
            npc["whispers"].messages[0] = [player.name + "...", player.name + "...", "...your destiny awaits.",
                                           "Follow the whispers of the wind, and come to me.", "Secrets untold and"
                                           " challenges unknown lie ahead.", "Trust in the unseen path...",
                                           "... come to me."]

            # Dragon Firefrost setting.
            npc["dragon firefrost"].messages = [player.name + "...",
                                                "You finally come to me...",
                                                "Destiny calls ""for a dance of fire and frost between us...",
                                                "Ready your blade..."]

            # Introduction.
            if player.name:
                screen = talk(npc=npc["whispers"], player=player)

        elif choice == "2":  # Load game choice.
            try:
                clear()
                disp_title()
                print(" < LOAD GAME >")
                print()

                # Loading inventory, user stats and map settings.
                player = import_player("cfg_save.pkl")
                load_setting = import_settings("cfg_setting.pkl")
                load_hash = load_dict_from_txt("cfg_hash.txt")
                if get_hash("cfg_save.pkl") != load_hash["hash"]:
                    raise OSError

                load_map_set(map_set, load_setting["ms"])
                npc.update(load_setting["npc"])

                x = player.x
                y = player.y
                player.place = map_set[coordstr(x, y)]
                player.outside = True

                menu = False
                play = True

                print(" Welcome back " + player.name + ".")
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

    time_init = datetime.now()
    while play:
        player.x = x
        player.y = y

        save(player, npc, map_set, time_init)  # Autosave.
        time_init = datetime.now()
        clear()

        # Fight chances of moving, and player status refreshing.
        if not standing:
            # Fight.
            if player.place.fight:
                if random.randint(a=0, b=100) < max(player.place.mobs_chances):
                    enemy = random.choices(player.place.mobs, player.place.mobs_chances, k=1)[0]
                    play, menu, win = battle(player, mobs[enemy].copy(), map_set)
                    save(player, npc, map_set, time_init)

            # Player status refresh.
            player.refresh_status()

        # Lvl upgrade of user.
        if player.exp >= player.expmax:
            player.lvl += 1
            player.exp = 0
            player.expmax = 10 * player.lvl
            player.b_hpmax += 2
            player.b_attack += 0.4
            player.b_defense += 0.20
            player.b_precision += 0.005
            player.b_evasion += 0.01
            player.st_points += 3
            screen = "You have lvl up. ASSIGN Strength/Agility/Vitality. You can assign 3 points."

        # Refreshing stats of user.
        items_stats = sum_item_stats(player.equip)
        player.hpmax = player.b_hpmax + player.vitality * 2
        player.attack = player.b_attack + int(player.strength * 0.4) + items_stats["atk"]
        player.defense = player.b_defense + int(player.resistance * 0.4) + items_stats["def"]
        player.evasion = player.b_evasion + player.agility * 0.01 + items_stats["eva"]
        player.precision = player.b_precision + player.agility * 0.005 + items_stats["pre"]

        if play:
            # Setting enviroment variables.
            # Location description setting.
            location, loc_des = player.place.name, player.place.description

            # Day time and day moment.
            day_time, day_moment = day_est(day_time, add_hs)
            add_hs = 0

            # Draw of general stats.
            clear()
            disp_play(player, location, "NAIWAT", day_moment, loc_des, x, y,
                      draw_move(x, y, x_len, y_len, player, tile_map, map_set), screen, 36)

            # Input action.
            print()
            action = input(" " * 2 + "# ").lower().split()
            if not action:
                action = ["None"]

            # Action ejecution.
            if action[0] == "0":  # Save game.
                play = False
                menu = True
                save(player, npc, map_set, time_init)

            if action[0] in ["1", "2", "3", "4"]:  # Move action.
                if player.outside:
                    screen, x, y, add_hs, standing = move(x, y, x_len, y_len, player, tile_map, action[0], map_set)
                    player.place = map_set[coordstr(x, y)]
                else:
                    screen = "You are in " + player.place.name.title().replace("'S", "'s")

            elif action[0] in ["5", "6"]:  # Fast use object action.
                if action[0] == "5":
                    screen, _ = use(player, player.slot1)
                if action[0] == "6":
                    screen, _ = use(player, player.slot2)
                standing = True

            elif action[0] == "assign":  # Assign action.
                if len(action) < 2:
                    screen = disp_assign(player.st_points)
                elif player.st_points:
                    if action[1] in ["strength", "str"]:
                        player.strength += 1
                        player.st_points -= 1
                        screen = "You have assigned a skill point to strength."
                    elif action[1] in ["agility", "agi"]:
                        player.agility += 1
                        player.st_points -= 1
                        screen = "You have assigned a skill point to agility."
                    elif action[1] in ["resistance", "res"]:
                        player.resistance += 1
                        player.st_points -= 1
                        screen = "You have assigned a skill point to resistance."
                    # elif action[1] in ["dexterity", "dex"]:
                    #     user_stats["b_dex"] += 1
                    #     user_stats["hability_points"] -= 1
                    #     screen = "You have assigned a skill point to dexterity."
                    elif action[1] in ["vitality", "vit"]:
                        player.vitality += 1
                        player.st_points -= 1
                        screen = "You have assigned a skill point to vitality."
                elif player.st_points == 0:
                    screen = "You have no more skill points left."
                else:
                    "That is not posible."
                standing = True

            elif action[0] == "check":  # Check action.
                screen = check(player.place, " ".join(action[1:]))

            elif action == ["draw", "map"]:  # Update of map action.
                player.map[y][x] = player.place.color
                if x != 0:
                    player.map[y][x - 1] = map_set[coordstr(x - 1, y)].color
                if x != x_len:
                    player.map[y][x + 1] = map_set[coordstr(x + 1, y)].color
                if y != 0:
                    player.map[y - 1][x] = map_set[coordstr(x, y - 1)].color
                if y != y_len:
                    player.map[y + 1][x] = map_set[coordstr(x, y + 1)].color
                screen = "You have explored the area and mapped it out."

                if "telescope" in player.inventory.items.keys() and player.inventory.items["telescope"] >= 0:
                    # Explore a square instead of a cross
                    for i in range(max(0, x - 1), min(x_len, x + 2)):
                        for j in range(max(0, y - 1), min(y_len, y + 2)):
                            player.map[j][i] = map_set[coordstr(i, j)].color

            elif action[0] == "drop":  # Drop action.
                try:  # Converting input in proper clases and form.
                    item_name = " ".join(action[2:])
                    quantity = int(action[1])

                    screen = drop(player, item_name, quantity)  # Doing drop action.
                    standing = True

                except ValueError:
                    screen = disp_drop()  # Printing drop instructions.
                except IndexError:
                    screen = disp_drop()  # Printing drop instructions.

            elif action[0] == "enter":  # Enter action.
                if len(action) <= 2:
                    screen = disp_enter(player.place)
                    standing = True
                elif "_".join(action[2:]) in player.place.entries:
                    screen, fight = enter(x, y, "_".join(action[2:]), player)
                    if fight:
                        play, menu, win = battle(player, mobs["orc"].copy(), map_set)
                        if not play:
                            save(player, npc, map_set, time_init)
                    x, y = player.x, player.y
                    standing = True
                else:
                    screen = "There is no " + " ".join(action[2:]) + "."
                    standing = True

            elif action[0] in ["equip"] or action == ["show", "equip"]:  # Equip action.
                if len(action) <= 1:
                    screen = disp_equip(player.equip)
                    standing = True
                else:
                    screen = equip(player, " ".join(action[1:]))
                    standing = True

            elif action[0] == "exit":  # Exit entrie action:
                if not player.outside:
                    screen = "You left the " + player.place.name + "."
                    if hasattr(player.place.leave_entry, "leave_entry"):
                        player.place = player.place.leave_entry
                    else:
                        player.place = player.place.leave_entry
                        player.outside = True
                else:
                    screen = "You are outside."
                standing = True

            elif action[0] == "explore":  # Explore action:
                screen = explore(x, y, map_set)
                standing = False

            elif action[0] == "land":  # Land action.
                screen = land(x, y, player, map_set, tile_map)
                standing = False

            elif action[0] == "listen":  # Listen action.
                screen = "You don't hear anything special."

            elif action == ["look", "around"]:  # Look around action.
                screen = disp_look_around(player.place)

            elif action[0] in ["map"] or action == ["show", "map"]:  # Show map.
                player.map[y][x] = globals.PINK
                plt.figure(player.name + "'s map")
                plt.imshow(player.map)
                plt.title("Map")
                plt.show()
                player.map[y][x] = player.place.color
                standing = True

            elif action[:2] == ["pick", "up"]:  # Pick up action.
                screen = pick_up(player, "_".join(action[2:]))

            elif action == ["show", "inventory"] or action[0] in ["inventory", "inv"]:
                screen = disp_show_inventory(player)
                standing = True

            elif action[0] == "slot1":  # Selection slot1 action.
                item_select = "_".join(action[1:])
                if item_select in globals.ITEMS_SELL and item_select in player.inventory.items.keys():
                    player.slot1 = " ".join(action[1:]).title()
                standing = True

            elif action[0] == "slot2":  # Selection slot1 action.
                item_select = "_".join(action[1:])
                if item_select in globals.ITEMS_SELL and item_select in player.inventory.items.keys():
                    player.slot2 = " ".join(action[1:]).title()
                standing = True

            elif action[0] == "sleep":  # Sleep action.
                if len(action) <= 2:
                    screen = disp_sleep(x, y, player.place)
                    standing = True
                else:
                    screen, player.hp, day_time, day_moment = sleep_in_bed(player.place, player.hp, player.hpmax,
                                                                           day_time, action[2])
                    player.x_cp, player.y_cp = x, y
                    standing = True

            elif action[0] == "talk":  # Talk action.
                npc_name = " ".join(action[2:]).lower()
                if len(action) <= 2:
                    screen = disp_talk(player.place)
                    standing = True
                elif npc_name in player.place.npc:
                    screen = talk(npc=npc[npc_name], player=player)
                    standing = True
                else:
                    screen = "Here no one is called " + npc_name.title() + "."
                    standing = True

            elif action[0] == "unequip":  # Unequip action.
                if len(action) <= 1:
                    screen = disp_equip(player.equip)
                    standing = True
                else:
                    screen = unequip(player, " ".join(action[1:]))
                    standing = True

            elif action == ["use", "boat"]:  # Use boat action.
                screen = use_boat(x, y, player, map_set)
                standing = True

            elif action[0] in ["use"]:  # Fast use object action.
                screen, _ = use(player, "_".join(action[1:]))
                standing = True

            elif action[0] == "wait":  # Wait action.
                if len(action) <= 2:
                    screen = disp_wait()
                    standing = True
                else:
                    screen, day_time, day_moment = wait(day_time, action[2])
                    standing = False

            # Admin commans.
            elif action[0] == "teleport":
                x = int(action[1])
                y = int(action[2])
                player.place = map_set[coordstr(x, y)]
                standing = True
                screen = "You teleported to " + str(x) + " " + str(y) + "."

            elif action == ["time", "played"]:
                player.refresh_time_played(datetime.now(), time_init)
                screen = str(player.time_played)

            elif action == ["map_set"]:
                for i in range(len(tile_map)):
                    for j in range(len(tile_map[i])):
                        key = coordstr(j, i)
                        print(key, map_set[key].name, map_set[key].description)

            elif action[0] == "update":  # Admin action for update de game while devolping.
                #
                # map_set.updatplayer.exp += 1000
                #                 # player.inventory.add_item("telescope", 1)
                #                 # player.inventory.add_item("torch", 1)
                #                 # player.inventory.add_item("gold", 100)e(globals.MAP_SETTING_INIT)
                # player.events["message"] = False
                # player.events["permission"] = False
                # npc["fisherman marlin"][3][0] = True
                player.inventory.add_item(item="antidote", quantity=1)
                screen = "Map updated."
            else:
                standing = True

            # Event handler.
            npc, map_set, play, menu = event_handler(player, npc, map_set, mobs, time_init, play, menu)
