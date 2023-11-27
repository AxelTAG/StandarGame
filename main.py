# Imports.
import os
import random
import numpy as np
import matplotlib.pyplot as plt
from utils import label_pixels, draw_move, tl_map_set, day_est, export_dict_to_txt, load_dict_from_txt, clear
import globals
from displays import disp_play, disp_sleep, disp_talk, disp_title, disp_wait
from actions import move, use_boat, land, sleep_in_bed, wait, talk


def draw():
    print("-+------------------+-")


def save():
    global player_map, map_set
    save_list = [
        NAME,
        str(HP),
        str(HPMAX),
        str(LVL),
        str(EXP),
        str(EXPMAX),
        str(ATK),
        str(inventory["red_potions"]),
        str(inventory["elixirs"]),
        str(inventory["gold"]),
        str(x),
        str(y),
    ]

    with open("load.txt", "w") as file_txt:
        for item in save_list:
            file_txt.write(item + "\n")

    np.savetxt("load_map.txt", player_map.reshape(-1, player_map.shape[-1]), fmt='%d', delimiter='\t')

    export_dict_to_txt({0: inventory, 1: map_set}, "cfg_save.txt")


def heal(amount):
    global HP
    if HP + amount < HPMAX:
        HP += amount
    else:
        HP = HPMAX
    print(NAME + "'s HP refilled to " + str(HP) + "!")


def battle(enemies, probs):
    global fight, play, run, HP, inventory, boss, EXP

    if not boss:
        enemy = random.choices(enemies, weights=probs, k=1)[0]
    else:
        enemy = "Dragon"
    hp = mobs[enemy]["hp"]
    hpmax = hp
    atk = mobs[enemy]["at"]
    g = mobs[enemy]["go"]
    e = mobs[enemy]["exp"]

    while fight:
        clear()
        draw()
        print(" Defeat the " + enemy.title() + "!")
        draw()
        print(" " + enemy.title() + "'s HP: " + str(hp) + "/" + str(hpmax))
        print(" " + NAME + "'s HP: " + str(HP) + "/" + str(HPMAX))
        print(" POTIONS: " + str(inventory["red_potions"]))
        print(" ELIXIR: " + str(inventory["elixirs"]))
        draw()
        print(" 1 - ATTACK")
        if inventory["red_potions"] > 0:
            print(" 2 - USE POTION (30HP)")
        if inventory["elixirs"] > 0:
            print(" 3 - USE ELIXIR (50HP)")
        draw()

        choice_action = input(" # ")

        if choice_action == "1":
            hp -= ATK
            print(" " + NAME + " dealt " + str(ATK) + " damage to the " + enemy.title() + ".")
            if hp > 0:
                HP -= atk
                print(" " + enemy.title() + " dealt " + str(atk) + " damage to " + NAME + ".")
            input("> ")

        elif choice_action == "2":
            if inventory["red_potions"] > 0:
                inventory["red_potions"] -= 1
                heal(30)
                HP -= atk
                print(" " + enemy.title() + " dealt " + str(atk) + " damage to " + NAME + ".")
            else:
                print(" No potions!")
            input(" > ")

        elif choice_action == "3":
            if inventory["elixirs"] > 0:
                inventory["elixirs"] -= 1
                heal(50)
                HP -= atk
                print(" " + enemy.title() + " dealt " + str(atk) + " damage to " + NAME + ".")
            else:
                print(" No elixirs!")
            input(" > ")

        if HP <= 0:
            print(" " + enemy.title() + " defeated " + NAME + "...")
            draw()
            fight = False
            play = False
            run = False
            print(" GAME OVER")
            input(" > ")

        if hp <= 0:
            print(" " + NAME + " defeated the " + enemy.title() + "!")
            draw()
            fight = False
            inventory["gold"] += g
            EXP += e
            print(" You've found " + str(g) + " gold!")
            if random.randint(0, 100) < 30:
                inventory["red_potions"] += 1
                print(" You've found a potion!")
            if enemy == "Dragon":
                draw()
                print(" Congratulations, you've finished the game!")
                boss = False
                play = False
                run = False
            input(" > ")
            clear()


def shop():
    global buy, inventory, ATK

    while buy:
        clear()
        draw()
        print("Welcome to the shop!")
        draw()
        print("GOLD: " + str(inventory["gold"]))
        print("POTIONS: " + str(inventory["red_potions"]))
        print("ELIXIRS: " + str(inventory["elixirs"]))
        print("ATK: " + str(ATK))
        draw()
        print("1 - BUY POTION (30HP) - 5 GOLD")
        print("2 - BUY ELIXIR (MAXHP) - 8 GOLD")
        print("3 - UPGRADE WEAPON (+2ATK) - 10 GOLD")
        print("4 - LEAVE")
        draw()

        choice_action = input("# ")

        if choice_action == "1":
            if inventory["gold"] >= 5:
                inventory["red_potions"] += 1
                inventory["gold"] -= 5
                print("You've bought a potion!")
            else:
                print("Not enough gold!")
            input("> ")
        elif choice_action == "2":
            if inventory["gold"] >= 8:
                inventory["elixirs"] += 1
                inventory["gold"] -= 8
                print("You've bought an elixir!")
            else:
                print("Not enough gold!")
            input("> ")
        elif choice_action == "3":
            if inventory["gold"] >= 10:
                ATK += 2
                inventory["gold"] -= 10
                print("You've upgraded your weapon!")
            else:
                print("Not enough gold!")
            input("> ")
        elif choice_action == "4":
            buy = False


# Command line settings.
# os.system(f"mode con: cols={globals.WIDTH} lines={globals.HEIGHT}")

# Game variables.
run = True
menu = True
play = False
rules = False

# Play variables.
fight = False
standing = True
buy = False
speak = False
boss = False
day_time = 6
day_moment = "MORNING"
add_hs = 0

# Player variables.
NAME = ""
HP = 50
HPMAX = 50
LVL = 1
EXP = 0
EXPMAX = 10 * LVL
ATK = 3
x = 0
y = 0

# Player map.
player_map = np.zeros((32, 32, 4), dtype=np.uint8)
player_map[:, :, 3] = np.ones((32, 32), dtype=np.uint8) * 255

inventory = {}

tile_map = label_pixels("world_map.png")

map_set = tl_map_set(tile_map)

y_len = len(tile_map)-1
x_len = len(tile_map[0])-1

bioms = globals.BIOMS

npc = globals.NPC

e_list = ["goblin", "orc", "slime"]

mobs = globals.MOBS

screen = "."


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

        # Rules.
        if rules:
            clear()
            disp_title()

            print()
            print()
            print(" < RULES >")
            print()
            print(" I'm the creator of this game and these are the rules.")
            rules = False
            choice = ""
            input(" > ")
        else:
            choice = input(" # ")

        # New game choice.
        if choice == "1":
            clear()
            try:
                file = open("load.txt", "r").readlines()
                L_NAME = file[0][:-1]
                L_HP = int(file[1][:-1])
                L_HPMAX = int(file[2][:-1])
                L_LVL = int(file[3][:-1])
                L_EXP = int(file[4][:-1])
                L_EXPMAX = int(file[5][:-1])

                disp_title()

                print(" < NEW GAME >")
                print()
                print(" There is already a game existing, do you want to delete it?")
                print()
                print(" NAME: " + str(L_NAME) + " / LVL: " + str(L_LVL))
                print()
                print(" 1 - Yes")
                print(" 2 - No")
                action_choice = input(" # ")
                if action_choice == "2":
                    pass
                else:
                    NAME = input(" # What's your NAME, hero? ")
                    menu = False
                    play = True
            except OSError:
                NAME = input(" # What's your NAME, hero? ")
                menu = False
                play = True

                # Initial settings.
                # Inventory variables.
                inventory = {"red_potions": 1, "elixirs": 0, "gold": 5, "walk": True}
                # Map settings.
                map_set.update(globals.MAP_SETTING)

        # Load game choice.
        elif choice == "2":
            # Load basics stats.
            try:
                f = open("load.txt", "r")
                load_list = f.readlines()
                if len(load_list) == 12:
                    NAME = load_list[0][:-1]
                    HP = int(load_list[1][:-1])
                    HPMAX = int(load_list[2][:-1])
                    LVL = int(load_list[3][:-1])
                    EXP = int(load_list[4][:-1])
                    EXPMAX = int(load_list[5][:-1])
                    ATK = int(load_list[6][:-1])
                    inventory["red_potions"] = int(load_list[7][:-1])
                    inventory["elixirs"] = int(load_list[8][:-1])
                    inventory["gold"] = int(load_list[9][:-1])
                    x = int(load_list[10][:-1])
                    y = int(load_list[11][:-1])
                    clear()
                    disp_title()

                    print(" < LOAD GAME >")
                    print()
                    print(" Welcome back, " + NAME + "!")
                    input(" > ")
                    menu = False
                    play = True
                else:
                    print(" Corrupt save file!")
                    input(" > ")
            except OSError:
                print(" No loadable save file!")
                input(" > ")

            # Loading user map.
            try:
                map_load = np.loadtxt("load_map.txt", delimiter='\t', dtype=int)
                player_map = map_load.reshape((32, 32, 4))
            except OSError:
                print(" No loadable save file!")
                input(" > ")

            # Loading inventory and map settings.
            load_setting = load_dict_from_txt("cfg_save.txt")
            inventory.update(load_setting[0])
            map_set.update(load_setting[1])

        elif choice == "3":
            rules = True
        elif choice == "4":
            quit()

    while play:
        save()  # autosave
        clear()

        # Fight chances of moving.
        if not standing:
            if bioms[tile_map[y][x]]["e"]:
                if random.randint(0, 100) < max(bioms[tile_map[y][x]]["e_chance"]):
                    fight = True
                    battle(bioms[tile_map[y][x]]["e_list"], bioms[tile_map[y][x]]["e_chance"])

        if EXP >= EXPMAX:
            LVL += 1
            EXP = 0
            EXPMAX = 10 * LVL
            ATK += 1

        if play:
            # Setting enviroment variables.
            # Location setting.
            if y == 0 and x == 0:
                location = NAME + "'s Hut"
            else:
                location = bioms[tile_map[y][x]]["t"]

            # Location description setting.
            if map_set[(x, y)][1]:
                loc_des = map_set[(x, y)][1]
            else:
                loc_des = bioms[tile_map[y][x]]["d"]

            # Day time and day moment.
            day_time, day_moment = day_est(day_time, add_hs)
            add_hs = 0

            # Draw title.
            #print(" < GAME >")
            print()

            # Draw of general stats.
            disp_play(location, "NAIWAT", day_moment, loc_des, NAME, HP, HPMAX, LVL, EXP, EXPMAX, ATK,
                      inventory["red_potions"], inventory["elixirs"], inventory["gold"], x, y,
                      draw_move(x, y, x_len, y_len, inventory, tile_map), [], screen, 36)

            # Input action.
            print()
            action = input(" " * 2 + "# ").lower().split()
            if not action:
                action = ["None"]

            # Action ejecution.
            if action[0] == "0":  # Save game.
                play = False
                menu = True
                save()

            if action[0] in ["1", "2", "3", "4"]:  # Move action.
                text, x, y, add_hs = move(x, y, x_len, y_len, inventory, tile_map, action[0])
                screen = text
                standing = False

            elif action[0] == "5":  # Use potion.
                if inventory["red_potions"] > 0:
                    inventory["red_potions"] -= 1
                    heal(30)
                else:
                    print(" No potions!")
                input(" " * 4 + "> ")
                standing = True

            elif action[0] == "6":  # Use elixir.
                if inventory["elixirs"] > 0:
                    inventory["elixirs"] -= 1
                    heal(50)
                else:
                    print(" No elixirs!")
                input(" " * 4 + "> ")
                standing = True

            elif action[0] == "map":  # Show map.
                player_map[y][x] = globals.WHITE
                plt.figure(NAME + "'s map")
                plt.imshow(player_map)
                plt.title("Map")
                plt.show()
                player_map[y][x] = globals.BIOMS[tile_map[y][x]]["c"]
                standing = True

            elif action == ["draw", "map"]:  # Update of map action.
                player_map[y][x] = bioms[tile_map[y][x]]["c"]
                if x != 0:
                    player_map[y][x - 1] = bioms[tile_map[y][x - 1]]["c"]
                if x != x_len:
                    player_map[y][x + 1] = bioms[tile_map[y][x + 1]]["c"]
                if y != 0:
                    player_map[y - 1][x] = bioms[tile_map[y - 1][x]]["c"]
                if y != y_len:
                    player_map[y + 1][x] = bioms[tile_map[y + 1][x]]["c"]

            elif action[0] == "sleep":  # Sleep action.
                if len(action) <= 2:
                    screen = disp_sleep(x, y, map_set)
                    standing = True
                else:
                    screen, HP, day_time, day_moment = sleep_in_bed(x, y, map_set, HP, HPMAX, day_time, action[2])
                    standing = True

            elif action[0] == "wait":  # Wait action.
                if len(action) <= 2:
                    screen = disp_wait()
                    standing = True
                else:
                    screen, day_time, day_moment = wait(day_time, action[2])
                    standing = False

            elif action == ["use", "boat"]:  # Use boat action.
                screen, inventory, map_set = use_boat(x, y, inventory, map_set)
                standing = True

            elif action[0] == "land":  # Land action.
                screen, inventory, map_set = land(x, y, inventory, map_set, tile_map)

            elif action[0] == "talk":  # Talk action.
                if len(action) <= 2:
                    screen = disp_talk(x, y, map_set)
                    standing = True
                elif " ".join(action[2:]) in map_set[(x, y)][2]:
                    talk(action[2:], npc[" ".join(action[2:])][0])
                    standing = True
                else:
                    screen = "Here no one is called " + " ".join(action[2:]) + "."
                    standing = True

            else:
                standing = True
