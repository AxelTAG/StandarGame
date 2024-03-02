# Imports.
# External imports.
import random
import numpy as np
import matplotlib.pyplot as plt

# Locals imports.
from actions import move, equip, use_boat, land, sleep_in_bed, wait, talk, enter, explore, battle, heal, unequip,\
    drop, use, check
from displays import disp_play, disp_sleep, disp_talk, disp_title, disp_wait, disp_enter, disp_assign, disp_equip,\
    disp_show_inventory, disp_drop, disp_look_around
import globals
from management import save, event_handler
from player import Player
from utils import import_player, label_pixels, draw_move, tl_map_set, day_est, load_dict_from_txt, clear, \
    check_name, get_hash, sum_item_stats

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
player = Player()

x = player.x  # X location.
y = player.y  # Y location.

inventory = player.inventory  # Inventory.

# Player map.
user_map = np.zeros((32, 32, 4), dtype=np.uint8)
user_map[:, :, 3] = np.ones((32, 32), dtype=np.uint8) * 255

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

                    # Player map.
                    user_map = np.zeros((32, 32, 4), dtype=np.uint8)
                    user_map[:, :, 3] = np.ones((32, 32), dtype=np.uint8) * 255

                    # Global settings.
                    tile_map = label_pixels("world_map.png")
                    map_set = tl_map_set(tile_map)
                    y_len = len(tile_map) - 1
                    x_len = len(tile_map[0]) - 1

                    bioms = globals.BIOMS.copy()
                    npc = globals.NPC.copy()
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
            map_set.update(globals.MAP_SETTING)
            # Location setting.
            map_set[str((x, y))]["t"] = player.name + "'s Hut"
            # Introduction setting.
            npc["whispers"][0] = [player.name + "...", player.name + "...", "...your destiny awaits.",
                                  "Follow the whispers of the wind, and come to me.", "Secrets untold and challenges "
                                  "unknown lie ahead.", "Trust in the unseen path...", "... come to me."]

            # Dragon Firefrost setting.
            npc["dragon firefrost"][0] = [player.name + "...", "You finally come to me...", "Destiny calls "
                                         "for a dance of fire and frost between us...", "Ready your blade..."]

            # Introduction.
            if player.name:
                screen, inventory = talk(npc=npc["whispers"], npc_name="Whispers", inventory=inventory)


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
                player = import_player("cfg_save.pkl")
                load_setting = load_dict_from_txt("cfg_save.txt")
                load_hash = load_dict_from_txt("cfg_hash.txt")
                if get_hash("cfg_save.pkl") != load_hash["hash"]:
                    raise OSError

                npc.update(load_setting["2"])
                map_set.update(load_setting["9"])

                x = player.x
                y = player.y

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

    while play:
        player.x = x
        player.y = y
        save(player, user_map, npc, map_set)  # Autosave.
        clear()

        # Fight chances of moving.
        if not standing:
            if map_set[str((x, y))]["e"]:
                if random.randint(0, 100) < max(bioms[tile_map[y][x]]["e_chance"]):
                    enemy = random.choices(bioms[tile_map[y][x]]["e_list"], bioms[tile_map[y][x]]["e_chance"], k=1)[0]
                    play, menu, win = battle(player, mobs[enemy].copy(), map_set)
                    save(player, user_map, npc, map_set)

        # Lvl upgrade of user.
        if player.exp >= player.expmax:
            player.lvl += 1
            player.exp = 0
            player.expmax = 10 * player.lvl
            player.b_hpmax += 2
            player.b_attack += 0.4
            player.b_defense += 0.025
            player.b_precision += 0.005
            player.b_evasion += 0.01
            screen = "You have lvl up. ASSIGN Strength/Agility/Vitality. You can assign 3 points."
            player.st_points += 3

        # Refreshing stats of user.
        items_stats = sum_item_stats(player.equip)
        player.hpmax = player.b_hpmax + player.vitality * 2
        player.attack = player.b_attack + int(player.strength * 0.4) + items_stats["atk"]
        player.defense = player.b_defense + int(player.resistance * 0.4) + items_stats["def"]
        player.evasion = player.b_evasion + player.agility * 0.01 + items_stats["eva"]
        player.precision = player.b_precision + player.agility * 0.005 + items_stats["pre"]

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
                save(player, user_map, npc, map_set)

            if action[0] in ["1", "2", "3", "4"]:  # Move action.
                screen, x, y, add_hs, standing = move(x, y, x_len, y_len, player, tile_map, action[0], map_set)

            elif action[0] in ["5", "6"]:  # Fast use object action.
                if action[0] == "5":
                    fast_object = player.slot1
                if action[0] == "6":
                    fast_object = player.slot2
                screen, object_used = use(player, fast_object)
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

                if "telescope" in player.inventory.items.keys() and player.inventory.items["telescope"] >= 0:
                    # Explore a square instead of a cross
                    for i in range(max(0, x - 1), min(x_len, x + 2)):
                        for j in range(max(0, y - 1), min(y_len, y + 2)):
                            user_map[j][i] = bioms[tile_map[j][i]]["c"]

            elif action[0] == "drop":  # Drop action.
                if len(action) <= 2:
                    screen = disp_drop()
                    standing = True
                else:
                    screen, player = drop(player, " ".join(action[2:]), int(action[1]))

            elif action[0] == "enter":  # Enter action.
                if len(action) <= 2:
                    screen = disp_enter(x, y, map_set)
                    standing = True
                elif " ".join(action[2:]) in map_set[str((x, y))]["entries"]:
                    screen, x, y, fight = enter(x, y, " ".join(action[2:]), player)
                    if fight:
                        play, menu, win = battle(player, mobs["orc"].copy(), map_set)
                        if not play:
                            save(player, user_map, npc, map_set)
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

            elif action[0] == "explore":  # Explore action:
                screen, map_set = explore(x, y, map_set)
                standing = False

            elif action[0] == "land":  # Land action.
                screen, map_set = land(x, y, player, map_set, tile_map)
                standing = False

            elif action[0] == "listen":  # Listen action.
                screen = "You don't hear anything special."

            elif action == ["look", "around"]:  # Look around action.
                screen = disp_look_around(player, map_set)

            elif action[0] in ["map"] or action == ["show", "map"]:  # Show map.
                user_map[y][x] = globals.PINK
                plt.figure(player.name + "'s map")
                plt.imshow(user_map)
                plt.title("Map")
                plt.show()
                user_map[y][x] = globals.BIOMS[tile_map[y][x]]["c"]
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

            elif action == ["show", "inventory"] or action[0] in ["inventory", "inv"]:
                screen = disp_show_inventory(player)
                standing = True

            elif action[0] == "sleep":  # Sleep action.
                if len(action) <= 2:
                    screen = disp_sleep(x, y, map_set)
                    standing = True
                else:
                    screen, player.hp, day_time, day_moment = sleep_in_bed(x, y, map_set, player.hp, player.hpmax, day_time, action[2])
                    player.x_cp, player.y_cp = x, y
                    standing = True

            elif action[0] == "talk":  # Talk action.
                npc_name = " ".join(action[2:]).lower()
                if len(action) <= 2:
                    screen = disp_talk(x, y, map_set)
                    standing = True
                elif npc_name in map_set[str((x, y))]["npc"]:
                    screen = talk(npc=npc[npc_name], npc_name=npc_name, player=player)
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
                screen, map_set = use_boat(x, y, player, map_set)
                standing = True

            elif action[0] in ["use"]:  # Fast use object action.
                screen, object_used = use(player, "_".join(action[1:]))
                standing = True

            elif action[0] == "wait":  # Wait action.
                if len(action) <= 2:
                    screen = disp_wait()
                    standing = True
                else:
                    screen, day_time, day_moment = wait(day_time, action[2])
                    standing = False

            elif action[0] == "update":  # Admin action for update de game while devolping.
                #player.exp += 1000
                map_set.update(globals.MAP_SETTING)
                npc.update(globals.NPC)
                player.events["message"] = False
                player.events["permission"] = False
                screen = "Map updated."
                npc["fisherman marlin"][3][0] = True
            else:
                standing = True

            # Event handler.
            npc, map_set, play, menu = event_handler(player, user_map, npc, map_set, mobs, play, menu)
