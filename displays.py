# Imports.
# Locals imports.
import globals

from biome import Biome
from enums import Months
from map import Map
from mob import Mob
from player import Player
from utils import clear, get_label, patron_print, text_2_col, text_ljust, typewriter


# Assign display.
def disp_assign(st: int) -> str:
    return f"Assign skill point ({st}) to:\n- Strength (STR)\n- Agility (AGI)\n- Resistance (RES)\n- Vitality (V IT)"


def disp_attack() -> str:
    return "Use ATTACK ENEMY to attack an enemy."


# Bar display
def disp_bar(n: int = 18, disp: bool = True) -> str:
    text = "--" + "-" * n + "--"
    if disp:
        print(text)

    return text


# Battle display.
def disp_battle(player: Player, enemy: Mob, text: str) -> None:
    width = 36
    clear()
    disp_title()
    print(" < GAME >")
    print()

    # Text lines for text1.
    u_name = player.name
    u_hp = "\n HP: " + str(int(player.hp)) + " / " + str(player.hpmax)
    u_hpbar = "\n " + "█" * int(25 * (player.hp / player.hpmax)) + "-" * (
            25 - int(25 * (max(player.hp, 0) / player.hpmax))) + "|"
    u_atk = "\n ATTACK: " + str(int(player.attack))

    # Text lines for text2.
    e_name = "ENEMY: " + enemy.name
    e_hp = "\n HP: " + str(int(enemy.hp)) + " / " + str(enemy.hpmax)
    e_hpbar = "\n " + "█" * int(25 * (enemy.hp / enemy.hpmax)) + "-" * (
            25 - int(25 * (max(enemy.hp, 0) / enemy.hpmax))) + "|"

    # Text lines for text3.
    o_escape = "0 - ESCAPE"
    o_attack = "\n1 - ATTACK"

    slot1_quantity = str(player.inventory.items[player.slot1]) if player.has(player.slot1) else "0"
    slot2_quantity = str(player.inventory.items[player.slot2]) if player.has(player.slot2) else "0"
    o_slot1 = "\n 2 - " + player.slot1.replace("_", " ").upper() + " [" + slot1_quantity + "]"
    o_slot2 = "\n 3 - " + player.slot2.replace("_", " ").upper() + " [" + slot2_quantity + "]"

    text1 = u_name + u_hp + u_hpbar + u_atk
    text2 = e_name + e_hp + e_hpbar
    text3 = o_escape + o_attack + o_slot1 + o_slot2
    text4 = text

    cmp_text = []
    cmp_text = cmp_text + text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "-")
    cmp_text = cmp_text + text_2_col(text1, text2, width, "|")
    cmp_text = cmp_text + text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "+")
    cmp_text = cmp_text + text_2_col(text3, text4, width, "|")
    cmp_text = cmp_text + text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "+")

    for line in cmp_text:
        print(" " + line)


# Disp drop.
def disp_drop() -> str:
    return "DROP -QUANTITY -ITEM."


# Enter action.
def disp_enter(place: Biome) -> str:
    if place.entries:
        msg = "You want to enter to:"
        n = 0
        for entrie_key, entrie in place.entries.items():
            if type(entrie) == Biome or entrie.hide["visibility"]:
                entrie_name = " ".join(entrie_key.split("_")).title()
                msg += f"\n - {entrie_name}"
                n += 1
            else:
                continue
        if n < 1:
            return "There aren't entries here."
        return msg
    else:
        return "There aren't entries here."


# Equip display.
def disp_equip(equip: dict) -> str:
    text = "EQUIP:"
    for body_part, item in equip.items():
        body_part_name = body_part.name.replace('_', ' ').title()

        if equip[body_part] is not None:
            text += f"\n- {body_part_name}: {item.name}."
        else:
            text += f"\n- {body_part_name}: None."
    return text


def disp_intro(width: int = 60) -> None:
    disp_logo(width=width)
    print(" < PRESS ENTER > ".center(width))


def disp_load_game() -> None:
    print(" < LOAD GAME >")
    print()


def disp_logo(width: int = 80) -> None:
    logo = """
                                             #   
                              ++    ######   
                   #      +#   ##########    
                 ##     #- +#############    
                ###  ## .#####   -#######    
               #########                #    
               -####### #########            
              -########  ################    
              #######   #    ############    
             ######## ####  #   #######      
            ########  #######     ###        
          ######    ## #########    #        
      ######     ###  # ##########           
  #######   #########    ########            
 ####+    ############+   ####               
 ###  .################   ##                 
  #   ##################                     
  #  ######+######                           
 -  #+                                       
 """
    logo_lines = logo.split(sep="\n")
    for line in logo_lines:
        print(line.center(width))


def disp_main_screen():
    print(" < MENU >")
    print()
    print(" 1 - NEW GAME")
    print(" 2 - LOAD GAME")
    print(" 3 - RULES")
    print(" 4 - OPTIONS")
    print(" 5 - QUIT GAME")
    print()


def disp_new_game(existent_player: Player = None) -> None:
    if existent_player is None:
        print(" < NEW GAME >")
        print()
    else:
        print(" < NEW GAME >")
        print()
        print(" There is already a game existing, do you want to delete it?")
        print()
        print(f" NAME: {existent_player.name} / LVL: {existent_player.lvl}")
        print()
        print(" 1 - Yes")
        print(" 2 - No")
        print()


# Look around action.
def disp_look_around(place: Biome) -> str:
    items = place.items
    mobs = place.mobs_respawned

    if not items and not mobs:
        return "Nothing special here."

    text = "You have looked around and found:"
    if items:
        for item in items:
            text += "\n - " + item.replace("_", " ").title() + "."

    if mobs:
        for mob in mobs:
            text += "\n - " + mob.replace("_", " ").title() + "."
    return text


# Play display.
def disp_play(player: Player,
              map_game: Map,
              reg: str,
              x: int,
              y: int,
              mdir: list,
              screen_text: str,
              width: int) -> None:
    print("  .--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--. ")
    print(
        " / .. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\")
    print(
        " \\ \\/\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ \\/ /")
    print("  \\/ /`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'\\/ / ")
    t_loc = "LOCATION: " + player.place.name.upper()
    t_reg = "\n REGION: " + reg.upper()
    t_coord = "\n COORD: " + str(x) + " " + str(y)
    t_time = f"\n TIME OF DAY: {map_game.current_time_of_day_name.upper()} [{map_game.hour}HS]"
    t_week_day = f"\n WEEK DAY: {map_game.current_week_day_name.upper()} [{map_game.day} DAY]"
    t_month_year = f"\n MONTH: {Months(map_game.month).name.upper()} - YEAR: {map_game.year}"

    t_name = "NAME: " + player.name.upper()
    t_hp = "\nHP: " + str(int(player.hp)) + "/" + str(player.hpmax)
    t_hpbar = "\n|" + "█" * int(20 * (player.hp / player.hpmax)) + "-" * (
            20 - int(20 * (max(player.hp, 0) / player.hpmax))) + "|"
    t_lvl = "\nEXP: " + str(player.exp) + "/" + str(player.expmax) + " | LVL: " + str(player.lvl)
    t_expbar = "\n|" + "█" * int(11 * (player.exp / player.expmax)) + "-" * (
            11 - int(11 * (max(player.exp, 0) / player.expmax))) + "|"

    # Status text.
    t_status_types = []
    if player.poison > 0:
        t_status_types.append(f"POISONED [{player.poison}]")
    if player.hungry <= 10:
        t_status_types.append(f"HUNGRY")
    if player.thirsty <= 10:
        t_status_types.append(f"THIRSTY")
    if not t_status_types:
        t_status_types.append(f"HEALTHY")
    t_status = f"\nSTATUS: {' '.join(t_status_types)}"

    # Belt items.
    slot1_quantity = str(player.inventory.items[player.slot1]) if player.has(player.slot1) else "0"
    slot2_quantity = str(player.inventory.items[player.slot2]) if player.has(player.slot2) else "0"

    t_gold = "\nGOLD: " + str(player.inventory.gold)
    t_item1 = "\n5 - " + player.slot1.replace("_", " ").upper() + ": " + slot1_quantity
    t_item2 = "\n6 - " + player.slot2.replace("_", " ").upper() + ": " + slot2_quantity

    # Text4.1 lines.
    prim_stats = "PRIM. STATS: "
    t_atk = "\n\nATTACK:    " + str(int(player.attack))
    t_def = "\nDEFENSE:   " + str(int(player.defense))
    t_eva = "\nEVASION:   " + str(int(player.evasion * 100)) + "%"
    t_pre = "\nPRECISION: " + str(int(player.precision * 100)) + "%"
    t_weight = "\nWEIGHT:    " + str(int(player.current_weight)) + "/" + str(int(player.weight_carry))

    # Text4.2 lines.
    sec_stats = " SEC. STATS:"
    t_str = "\n\n STRENGTH:   " + str(int(player.strength))
    t_res = "\n RESISTANCE: " + str(int(player.resistance))
    t_agi = "\n AGILITY:    " + str(int(player.agility))
    # t_dex = "\n DEXTERITY:  " + str(int(user["b_dex"]))
    t_vit = "\n VITALITY:   " + str(int(player.vitality))

    text1 = t_loc + t_reg + t_coord + "\n." + t_time + t_week_day + t_month_year
    text2 = player.place.description
    text3 = t_name + t_lvl + t_expbar + t_hp + t_hpbar + t_status + t_gold
    text41 = prim_stats + t_atk + t_def + t_eva + t_pre + t_weight
    text42 = sec_stats + t_str + t_res + t_agi + t_vit
    text4 = "\n".join(text_2_col(text41, text42, int(width / 2 - 2), "|", False))
    text5 = "0 - SAVE AND QUIT"
    text6 = screen_text

    cmp_text = []
    cmp_text = cmp_text + text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "-")
    cmp_text = cmp_text + text_2_col(text1, text2, width, "|")
    cmp_text = cmp_text + text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "+")
    cmp_text = cmp_text + text_2_col(text3, text4, width, "|", False)
    cmp_text = cmp_text + text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "+")

    for i, status in enumerate(mdir):
        if i == 0:
            x_pos, y_pos = x, y - 1
        elif i == 1:
            x_pos, y_pos = x + 1, y
        elif i == 2:
            x_pos, y_pos = x, y + 1
        elif i == 3:
            x_pos, y_pos = x - 1, y
        else:
            x_pos, y_pos = x, y
        if status:
            text5 += "\n" + globals.DIRECTIONS[i] + " (" + get_label(x_pos, y_pos, player.map).upper() + ")"
    text5 += t_item1 + t_item2

    cmp_text = cmp_text + text_2_col(text5, text6, width, "|")
    cmp_text = cmp_text + text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "-")

    # cmp_text = concatenate_lists(cmp_text, side_text)
    patron = patron_print(globals.PATRON, len(cmp_text))

    for i, line in enumerate(cmp_text):
        print(" " + patron[i] + line + "  " + patron[i])


def disp_rules() -> None:
    print()
    print()
    print(" < RULES >")
    print()
    print(" I'm the creator of this game and these are the rules.")
    print()
    print(" 1) Follow your path.")
    print(" 2) Trace your path with: 'map' and 'draw map'.")
    print(" 3) Many actions are allowed ('use', 'enter', 'talk', 'look around', etc.), \n"
          "    and others you'll have to discover along your journey.")
    print(" 4) Remember: sleeping in a bed, will charge your energy.")
    print()


# Show inventory display.
def disp_show_inventory(player: Player):
    items = [(item, quantity) for item, quantity in player.inventory.items.items()]
    text = "INVENTORY:"
    for item, quantity in items:
        text += "\n - " + item.replace("_", " ").title() + ": " + str(quantity)
    text += "\n - Gold: " + str(player.inventory.gold)
    return text


# Sleep options display.
def disp_sleep(x: int, y: int, place: Biome) -> str:
    if "bed" in place.items:
        return "You want to sleep to:\n- Sleep to Morning\n- Sleep to Afternoon\n- Sleep to Evening\n- Sleep to Night"
    else:
        return "There is no bed here."


# Talk npc options.
def disp_talk(place) -> str:
    if place.npc:
        msg = "You want to talk to:"
        for i, npc in enumerate(place.npc):
            msg += "\n - " + npc.replace("_", " ").title()
        return msg
    else:
        return "No one is here."


def disp_talk_answers(answers):
    print()
    for i in range(len(answers.keys())):
        print(" " * 4 + str(i + 1), ") " + answers[i + 1].capitalize() + ".")
    print(" " * 4 + str(len(answers) + 1), ") Leave.")
    print()


# Talk display.
def disp_talk_util(npc_name: str) -> None:
    clear()
    disp_title()
    print(" < GAME >")
    print()
    print(" " * 4 + npc_name.title() + ":", end="\n ")
    print()


# Talk printing function.
def disp_talk_tw(npc, message):
    clear()
    # Printing of message.
    for line in message:
        disp_talk_util(npc.name)

        lines = text_ljust(line, width=70)
        for text in lines:
            typewriter(" " * 4 + text)
            print()

        input(" " * 4 + "> ")


# Title display.
def disp_title() -> None:
    title = ["  ___  ____|___|_________     ____|_____ ___                     ",
             " | ' ||    |   |___/___|_)        |__|__| ' |                    ",
             "\n",
             "  ___ ____ ____  ___  .-. _____       _  ________ ____/ ___ ____ ",
             " (   )_/(_)__|_)(   )(   )___/_    (_/ )|    __|_)    \\| ' |_/(_)",
             "  `-'            `|   `-'                                        "]
    print()
    for line in title:
        print(line)
    print()
    print()


# Wait options display.
def disp_wait() -> str:
    return "You want to wait to:\n- Wait to Morning\n- Wait to Afternoon\n- Wait to Evening\n- Wait to Nigth"
