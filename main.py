# Imports.
# External imports.
import random
import matplotlib.pyplot as plt
from datetime import datetime

# Locals imports.
import globals

from actions import drop, enter, equip, explore, land, move, sleep_in_bed, wait, talk, battle, pick_up,\
    unequip, use, use_boat, check, get_item, exit_entry
from displays import disp_play, disp_sleep, disp_talk, disp_title, disp_wait, disp_enter, disp_assign, disp_equip,\
    disp_show_inventory, disp_drop, disp_look_around
from enums import TimeOfDay
from management import event_handler, save
from map import Map
from player import Player
from utils import coordstr, import_player, import_settings, draw_move, load_dict_from_txt, clear, check_name, get_hash

# Game variables.
run = True
menu = True
play = False
rules = False

# Play variables.
fight = False
standing = True

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
                    standing = True

                    # Player variables.
                    player = Player()
                    inventory = player.inventory  # Inventory.

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

                player = Player()
                while not check_name(player.name):
                    player.name = input(" # What's your NAME, hero? ").title()
                menu = False
                play = True

            # Introduction of new game.
            if play:
                # Initial settings.
                # Map settings.
                map_game = Map()

                # Location setting.
                map_game.map_settings[coordstr(x=0, y=0)].entries["hut"].name = player.name + "'s Hut"
                player.place = map_game.map_settings[coordstr(x=0, y=0)].entries["hut"]

                # Introduction setting.
                map_game.npcs["whispers"].messages[0] = [player.name + "...", player.name + "...",
                                                         "...your destiny awaits.",
                                                         "Follow the whispers of the wind, and come to me.",
                                                         "Secrets untold and"
                                                         " challenges unknown lie ahead.",
                                                         "Trust in the unseen path...",
                                                         "... come to me."]

                # Dragon Firefrost setting.
                map_game.npcs["dragon firefrost"].messages = [player.name + "...", "You finally come to me...",
                                                              "Destiny calls ""for a dance of fire and frost between us...",
                                                              "Ready your blade..."]

                # Introduction.
                if player.name:
                    screen = talk(npc=map_game.npcs["whispers"], player=player, map_game=map_game)

        elif choice == "2":  # Load game choice.
            try:
                clear()
                disp_title()
                print(" < LOAD GAME >")
                print()

                # Loading inventory, user stats and map settings.
                player = import_player("cfg_save.pkl")
                map_game = import_player("cfg_map.pkl")
                load_setting = import_settings("cfg_setting.pkl")
                load_hash = load_dict_from_txt("cfg_hash.txt")
                if get_hash("cfg_save.pkl") != load_hash["hash"]:
                    raise OSError

                player.place = map_game.map_settings[coordstr(player.x, player.y)]
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
        # Autosave.
        save(player=player, map_game=map_game, npc=map_game.npcs, time_init=time_init)  # Autosave.
        time_init = datetime.now()
        clear()

        # Fight chances of moving, and player status refreshing.
        if not standing:
            # Fight.
            if player.place.fight and player.place.mobs:
                if random.randint(a=0, b=100) < max(player.place.mobs_chances):
                    enemy = random.choices(player.place.mobs, player.place.mobs_chances, k=1)[0]
                    play, menu, win = battle(player, mobs[enemy].copy(), map_game.map_settings)
                    save(player=player, map_game=map_game, npc=map_game.npcs, time_init=time_init)

            # Player status refresh.
            player.refresh_status()

        if play:
            # Draw of general stats.
            clear()
            disp_play(player=player,
                      map_game=map_game,
                      reg="NAIWAT",
                      x=player.x,
                      y=player.y,
                      mdir=draw_move(x=player.x,
                                     y=player.y,
                                     map_height=map_game.x_len,
                                     map_width=map_game.y_len,
                                     player=player,
                                     tl_map=map_game.map_labels,
                                     ms=map_game.map_settings),
                      screen_text=screen,
                      width=36)

            # Input action.
            print()
            action = input(" " * 2 + "# ").lower().split()
            if not action:
                action = ["None"]

            # Action ejecution.
            if action[0] == "0":  # Save game.
                play = False
                menu = True
                save(player=player, map_game=map_game, npc=map_game.npcs, time_init=time_init)

            if action[0] in ["1", "2", "3", "4"]:  # Move action.
                if player.outside:
                    screen, standing = move(player=player, map_game=map_game, mv=action[0])

                else:
                    screen = "You are in " + player.place.name.title().replace("'S", "'s")

            elif action[0] in ["5", "6"]:  # Fast use object action.
                if action[0] == "5":
                    screen, _ = use(player=player, item=player.slot1)
                if action[0] == "6":
                    screen, _ = use(player=player, item=player.slot2)
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
                if len(action) == 1:
                    screen = check(player=player, item=" ".join(action[1:]))

                elif action[1] in ["inv", "inventory"]:
                    screen = check(player=player, item="_".join(action[2:]), inventory=True)

                else:
                    screen = check(player=player, item="_".join(action[1:]))

            elif action == ["draw", "map"]:  # Update of map action.
                player.map[player.y][player.x] = map_game.map_settings[coordstr(x=player.x, y=player.y)].color
                if player.x != 0:
                    player.map[player.y][player.x - 1] = map_game.map_settings[coordstr(x=player.x - 1, y=player.y)].color
                if player.x != map_game.x_len:
                    player.map[player.y][player.x + 1] = map_game.map_settings[coordstr(x=player.x + 1, y=player.y)].color
                if player.y != 0:
                    player.map[player.y - 1][player.x] = map_game.map_settings[coordstr(x=player.x, y=player.y - 1)].color
                if player.y != map_game.y_len:
                    player.map[player.y + 1][player.x] = map_game.map_settings[coordstr(x=player.x, y=player.y + 1)].color
                screen = "You have explored the area and mapped it out."

                if "telescope" in player.inventory.items.keys() and player.inventory.items["telescope"] >= 0:
                    # Explore a square instead of a cross
                    for i in range(max(0, player.x - 1), min(map_game.x_len, player.x + 2)):
                        for j in range(max(0, player.y - 1), min(map_game.y_len, player.y + 2)):
                            player.map[j][i] = map_game.map_settings[coordstr(x=i, y=j)].color

            elif action[0] == "drop":  # Drop action.
                try:  # Converting input in proper clases and form.
                    item = "_".join(action[2:])
                    quantity = int(action[1])
                    screen = drop(player=player, item=item, quantity=quantity)  # Doing drop action.
                    standing = True

                except ValueError:
                    screen = disp_drop()  # Printing drop instructions.
                except IndexError:
                    screen = disp_drop()  # Printing drop instructions.

            elif action[0] == "enter":  # Enter action.
                if len(action) <= 2:
                    screen = disp_enter(player.place)
                    standing = True

                else:
                    screen, standing = enter(player=player, entrie="_".join(action[2:]))

            elif action[0] in ["equip"] or action == ["show", "equip"]:  # Equip action.
                if len(action) <= 1:
                    screen = disp_equip(player.equip)
                    standing = True

                else:
                    screen = equip(player=player, item="_".join(action[1:]))
                    standing = True

            elif action[0] == "exit":  # Exit entrie action:
                screen, standing = exit_entry(player=player, map_game=map_game)

            elif action[0] == "explore":  # Explore action:
                screen = explore(player=player, map_game=map_game)
                standing = False if player.outside else True

            elif action[0] == "land":  # Land action.
                screen = land(player=player, map_game=map_game)
                standing = False

            elif action[0] == "listen":  # Listen action.
                screen = "You don't hear anything special."

            elif action == ["look", "around"]:  # Look around action.
                screen = disp_look_around(player.place)

            elif action[0] in ["map"] or action == ["show", "map"]:  # Show map.
                player.map[player.y][player.x] = globals.PINK
                plt.figure(player.name + "'s map")
                plt.imshow(player.map)
                plt.title("Map")
                plt.show()
                player.map[player.y][player.x] = player.place.color
                standing = True

            elif action[:2] == ["pick", "up"]:  # Pick up action.
                screen = pick_up(player=player, item="_".join(action[2:]))

            elif action == ["show", "inventory"] or action[0] in ["inventory", "inv"]:
                screen = disp_show_inventory(player)
                standing = True

            elif action[0] == "slot1":  # Selection slot1 action.
                item_select = "_".join(action[1:])
                item_object = get_item(item_name=item_select)
                if item_object.consumable or item_object.equippable and item_select in player.inventory.items.keys():
                    player.slot1 = " ".join(action[1:]).title()
                else:
                    screen = f"You cannot equip {item_object.name} in the belt."
                standing = True

            elif action[0] == "slot2":  # Selection slot1 action.
                item_select = "_".join(action[1:])
                item_object = get_item(item_name=item_select)
                if item_object.consumable or item_object.equippable and item_select in player.inventory.items.keys():
                    player.slot2 = " ".join(action[1:]).title()
                else:
                    screen = f"You cannot equip {item_object.name} in the belt."
                standing = True

            elif action[0] == "sleep":  # Sleep action.
                if len(action) <= 2:
                    screen = disp_sleep(player.x, player.y, player.place)
                    standing = True

                else:
                    if action[2] in [tod.name.lower() for tod in TimeOfDay]:
                        screen = sleep_in_bed(player=player,
                                              map_game=map_game,
                                              time_of_day=TimeOfDay[action[2].upper()].value)
                        player.x_cp, player.y_cp = player.x, player.y
                        standing = True

                    else:
                        screen = f"{action[2].title()} is not a time of day."
                        standing = True

            elif action[0] == "talk":  # Talk action.
                npc_name = " ".join(action[2:]).lower()

                if len(action) <= 2:
                    screen = disp_talk(player.place)
                    standing = True

                elif npc_name in player.place.npc:
                    screen = talk(npc=map_game.npcs[npc_name], player=player, map_game=map_game)
                    standing = True

                else:
                    screen = f"Here no one is called {npc_name.title()}."
                    standing = True

            elif action[0] == "unequip":  # Unequip action.
                if len(action) <= 1:
                    screen = disp_equip(player.equip)
                    standing = True

                else:
                    screen = unequip(player=player, item="_".join(action[1:]))
                    standing = True

            elif action == ["use", "boat"]:  # Use boat action.
                screen = use_boat(player=player, map_game=map_game)
                standing = True

            elif action[0] == "use":  # Use object action.
                screen, _ = use(player, "_".join(action[1:]))
                standing = True

            elif action[0] == "wait":  # Wait action.
                if len(action) <= 2:
                    screen = disp_wait()
                    standing = True

                else:
                    if action[2] in [tod.name.lower() for tod in TimeOfDay]:
                        screen = wait(map_game=map_game,
                                      time_of_day=TimeOfDay[action[2].upper()].value)
                        standing = False
                    else:
                        screen = f"{action[2].title()} is not a time of day."
                        standing = True

            # --------------------------------------------------------------------------------------------------------

            # # Admin commands.
            elif action[0] == "estimate":  # Estimate date.
                screen = f"{map_game.estimate_date(days=int(action[1]))}"
                standing = True

            elif action[0] == "calendar":  # Calendar.
                screen = f"{map_game.day, map_game.month, map_game.year}"
                standing = True

            elif action[0] == "teleport":
                player.x = int(action[1])
                player.y = int(action[2])
                player.place = map_game.map_settings[coordstr(x=player.x, y=player.y)]
                standing = True
                screen = "You teleported to " + str(player.x) + " " + str(player.y) + "."

            elif action == ["time", "played"]:
                player.refresh_time_played(datetime.now(), time_init)
                screen = str(player.time_played)

            elif action == ["map_set"]:
                for i in range(len(map_game.map_settings)):
                    for j in range(len(map_game.map_labels[i])):
                        key = coordstr(j, i)
                        print(key, map_game.map_settings[key].name, map_game.map_settings[key].description)

            elif action == ["lvl", "up"]:
                player.lvl_up()

            elif action[:2] == ["add", "item"]:
                player.inventory.add_item(item=action[2], quantity=1)

            elif action[0] == "update":  # Admin action for update de game while devolping.
                #
                # map_set.updatplayer.exp += 1000
                #                 # player.inventory.add_item("telescope", 1)
                #                 # player.inventory.add_item("torch", 1)
                #                 # player.inventory.add_item("gold", 100)e(globals.MAP_SETTING_INIT)
                # player.events["message"] = False
                # player.events["permission"] = False
                # npc["fisherman marlin"][3][0] = True
                screen = "Map updated."
            else:
                standing = True

            # Event handler.
            map_game.npcs, map_game.map_settings, play, menu = event_handler(player, map_game, map_game.npcs, map_game.map_settings, mobs, time_init, play, menu)
