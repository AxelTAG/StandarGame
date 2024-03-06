# Imports.
# External imports.
import numpy as np

# Locals imports.
from utils import clear, get_label, patron_print, text_2_col
import globals
from player import Player


# Assign display.
def disp_assign(st: int) -> str:
    return "Assign skill point (" + str(st) + ") to:\n- Strength (STR)\n- Agility (AGI) \n- Resistance (RES) \n- Vitality (VIT)"


# Bar display
def disp_bar(n: int = 18, disp: bool = True) -> str:
    text = "--" + "-" * n + "--"
    if disp:
        print(text)
    return text


# Battle display.
def disp_battle(player: Player(), enemy: dict, text: str) -> None:
    width = 36
    clear()
    disp_title()
    print(" < GAME >")
    print()

    # Text lines for text1.
    u_name = player.name
    u_hp = "\n HP: " + str(int(player.hp)) + " / " + str(player.hpmax)
    u_hpbar = "\n " + "█" * int(25 * (player.hp / player.hpmax)) + "-" * (25 - int(25 * (max(player.hp, 0) / player.hpmax))) + "|"
    u_atk = "\n ATTACK: " + str(int(player.attack))

    # Text lines for text2.
    e_name = "ENEMY: " + enemy["name"]
    e_hp = "\n HP: " + str(int(enemy["hp"])) + " / " + str(enemy["hpmax"])
    e_hpbar = "\n " + "█" * int(25 * (enemy["hp"] / enemy["hpmax"])) + "-" * (25 - int(25 * (max(enemy["hp"], 0) / enemy["hpmax"]))) + "|"

    # Text lines for text3.
    o_escape = "0 - ESCAPE"
    o_attack = "\n1 - ATTACK"
    o_slot1 = "\n 2 - " + player.slot1.upper() + " [" + str(player.inventory.items[player.slot1.lower().replace(" ", "_")]) + "]"
    o_slot2 = "\n 3 - " + player.slot2.upper() + " [" + str(player.inventory.items[player.slot2.lower().replace(" ", "_")]) + "]"

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
def disp_enter(x: int, y: int, set_map: dict) -> str:
    if set_map[str((x, y))]["entries"]:
        msg = "You want to enter to:"
        for i, entrie in enumerate(set_map[str((x, y))]["entries"]):
            msg += "\n - " + entrie.title()
        return msg
    else:
        return "There aren't entries here."


# Equip display.
def disp_equip(equip: dict) -> str:
    text = "EQUIP:"
    for body_part, item in equip.items():
        if equip[body_part]:
            text += "\n- " + body_part.replace("_", " ").title() + ": " + item.replace("_", " ").title() + "."
        else:
            text += "\n- " + body_part.replace("_", " ").title() + ": " + str(item) + "."
    return text


# Look around action.
def disp_look_around(player: Player(), ms: dict) -> str:
    items = ms[str((player.x, player.y))]["items"]
    if items:
        text = "You have looked around and found:"
        for item in items:
            text += "\n - " + item.replace("_", " ").title() + "."
    else:
        text = "Nothing special here."
    return text


# Play display.
def disp_play(
        player: Player(), loc: str, reg: str, time: str, des: str, x: int, y: int, user_map: np.array,
        mdir: list, screen_text: str, width: int) -> None:
    print("  .--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--. ")
    print(" / .. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\")
    print(" \\ \\/\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ \\/ /")
    print("  \\/ /`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'\\/ / ")
    t_loc = "LOCATION: " + loc.upper()
    t_reg = "\n REGION: " + reg.upper()
    t_coord = "\n COORD: " + str(x) + " " + str(y)
    t_time = "\n TIME OF DAY: " + time.upper()
    t_name = "NAME: " + player.name.upper()
    t_hp = "\nHP: " + str(int(player.hp)) + "/" + str(player.hpmax)
    t_hpbar = "\n|" + "█" * int(20 * (player.hp / player.hpmax)) + "-" * (20 - int(20 * (max(player.hp, 0) / player.hpmax))) + "|"
    t_lvl = "\nEXP: " + str(player.exp) + "/" + str(player.expmax) + " | LVL: " + str(player.lvl)
    t_expbar = "\n|" + "█" * int(11 * (player.exp / player.expmax)) + "-" * (11 - int(11 * (max(player.exp, 0) / player.expmax))) + "|"
    t_gold = "\nGOLD: " + str(player.inventory.gold)
    t_item1 = "\n5 - " + player.slot1.replace("_", " ").upper() + ": " + str(player.inventory.items[player.slot1.lower().replace(" ", "_")])
    t_item2 = "\n6 - " + player.slot2.replace("_", " ").upper() + ": " + str(player.inventory.items[player.slot2.lower().replace(" ", "_")])

    # Text4.1 lines.
    prim_stats = "PRIM. STATS: "
    t_atk = "\n\nATTACK:    " + str(int(player.attack))
    t_def = "\nDEFENSE:   " + str(int(player.defense))
    t_eva = "\nEVASION:   " + str(int(player.evasion * 100)) + "%"
    t_pre = "\nPRECISION: " + str(int(player.precision * 100)) + "%"

    # Text4.2 lines.
    sec_stats = " SEC. STATS:"
    t_str = "\n\n STRENGTH:   " + str(int(player.strength))
    t_res = "\n RESISTANCE: " + str(int(player.resistance))
    t_agi = "\n AGILITY:    " + str(int(player.agility))
    # t_dex = "\n DEXTERITY:  " + str(int(user["b_dex"]))
    t_vit = "\n VITALITY:   " + str(int(player.vitality))

    text1 = t_loc + t_reg + t_coord + t_time + "\n." * 3
    text2 = des
    text3 = t_name + t_lvl + t_expbar + t_hp + t_hpbar + "\n." + t_gold
    text41 = prim_stats + t_atk + t_def + t_eva + t_pre
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
            text5 += "\n" + globals.DIRECTIONS[i] + " (" + get_label(x_pos, y_pos, user_map).upper() + ")"
    text5 += t_item1 + t_item2

    cmp_text = cmp_text + text_2_col(text5, text6, width, "|")
    cmp_text = cmp_text + text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "-")

    # cmp_text = concatenate_lists(cmp_text, side_text)
    patron = patron_print(globals.PATRON, len(cmp_text))

    for i, line in enumerate(cmp_text):
        print(" " + patron[i] + line + "  " + patron[i])


# Show inventory display.
def disp_show_inventory(player: Player()):
    items = [(item, quantity) for item, quantity in player.inventory.items.items() if not player.inventory.items[item] <= 0]
    text = "INVENTORY:"
    for item, quantity in items:
        text += "\n - " + item.replace("_", " ").title() + ": " + str(quantity)
    text += "\n - Gold: " + str(player.inventory.gold)
    return text


# Sleep options display.
def disp_sleep(x: int, y: int, set_map: dict) -> str:
    if "bed" in set_map[str((x, y))]["items"]:
        return "You want to sleep to:\n- Sleep to Morning\n- Sleep to Afternoon\n- Sleep to Evening\n- Sleep to Night"
    else:
        return "There is no bed here."


# Talk npc options.
def disp_talk(x: int, y: int, set_map: dict) -> str:
    if set_map[str((x, y))]["npc"]:
        msg = "You want to talk to:"
        for i, npc in enumerate(set_map[str((x, y))]["npc"]):
            msg += "\n - " + npc.title()
        return msg
    else:
        return "No one is here."


# Talk display.
def disp_talk_util(npc_name: str) -> None:
    clear()
    disp_title()
    print(" < GAME >")
    print()
    print(" " * 4 + npc_name.title() + ":", end="\n ")
    print()


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
