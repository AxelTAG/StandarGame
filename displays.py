# Imports.
from utils import text_ljust, text_2_col, concatenate_lists, patron_print, clear
import globals

# Constants.
DIRECTIONS = {0: "1 - NORTH",  1: "2 - EAST", 2: "3 - SOUTH", 3: "4 - WEST"}


# Assign display.
def disp_assign(user: dict) -> str:
    return "Assign skill point (" + str(user["hability_points"]) + ") to:\n- Strength (STR)\n- Agility (AGI)" \
                                                                   "\n- Resistance (RES)\n- Dexterity (DEX)"


# Bar display
def disp_bar(n: int = 18, disp: bool = True) -> str:
    text = "--" + "-" * n + "--"
    if disp:
        print(text)
    return text


# Battle display.
def disp_battle(user: dict, enemy: dict, text: str, inv: dict) -> None:
    width = 36
    clear()
    disp_title()
    print(" < GAME >")
    print()

    # Text lines for text1.
    u_name = user["name"]
    u_hp = "\n HP: " + str(int(user["hp"])) + " / " + str(user["hpmax"])
    u_hpbar = "\n " + "█" * int(25 * (user["hp"] / user["hpmax"])) + "-" * (25 - int(25 * (max(user["hp"], 0) / user["hpmax"]))) + "|"
    u_atk = "\n ATTACK: " + str(int(user["atk"]))

    # Text lines for text2.
    e_name = "ENEMY: " + enemy["name"]
    e_hp = "\n HP: " + str(int(enemy["hp"])) + " / " + str(enemy["hpmax"])
    e_hpbar = "\n " + "█" * int(25 * (enemy["hp"] / enemy["hpmax"])) + "-" * (25 - int(25 * (max(enemy["hp"], 0) / enemy["hpmax"]))) + "|"

    # Text lines for text3.
    o_attack = "1 - ATTACK"
    o_slot1 = "\n 2 - " + user["slot1"] + " [" + str(inv[user["slot1"].lower().replace(" ", "_")]) + "]"
    o_slot2 = "\n 3 - " + user["slot2"] + " [" + str(inv[user["slot2"].lower().replace(" ", "_")]) + "]"

    text1 = u_name + u_hp + u_hpbar + u_atk
    text2 = e_name + e_hp + e_hpbar
    text3 = o_attack + o_slot1 + o_slot2
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
def disp_look_around(user: dict, ms: dict) -> str:
    items = ms[str((user["x"], user["y"]))]["items"]
    if items:
        text = "You have looked around and found:"
        for item in items:
            text += "\n - " + item.replace("_", " ").title() + "."
    else:
        text = "Nothing special here."
    return text


# Play display.
def disp_play(
        user: dict, inventory: dict, loc: str, reg: str, time: str, des: str,
        item1: int, item2: int, x: int, y: int, mdir: list, slots: list[str], screen_text: str, width: int) -> None:
    print("  .--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--. ")
    print(" / .. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\")
    print(" \\ \\/\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ \\/ /")
    print("  \\/ /`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'\\/ / ")
    t_loc = "LOCATION: " + loc.upper()
    t_reg = "\n REGION: " + reg.upper()
    t_coord = "\n COORD: " + str(x) + " " + str(y)
    t_time = "\n TIME OF DAY: " + time.upper()
    t_name = "NAME: " + user["name"].upper()
    t_hp = "\nHP: " + str(int(user["hp"])) + "/" + str(user["hpmax"])
    t_hpbar = "\n|" + "█" * int(20 * (user["hp"] / user["hpmax"])) + "-" * (20 - int(20 * (max(user["hp"], 0) / user["hpmax"]))) + "|"
    t_lvl = "\nEXP: " + str(user["exp"]) + "/" + str(user["expmax"]) + " | LVL: " + str(user["lvl"])
    t_expbar = "\n|" + "█" * int(11 * (user["exp"] / user["expmax"])) + "-" * (11 - int(11 * (max(user["exp"], 0) / user["expmax"]))) + "|"
    t_gold = "\nGOLD: " + str(inventory["gold"])
    t_item1 = "\n5 - " + slots[0].replace("_", " ").upper() + ": " + str(inventory[slots[0].lower().replace(" ", "_")])
    t_item2 = "\n6 - " + slots[1].replace("_", " ").upper() + ": " + str(inventory[slots[1].lower().replace(" ", "_")])

    # Text4.1 lines.
    prim_stats = "PRIM. STATS: "
    t_atk = "\n\nATTACK:    " + str(int(user["atk"]))
    t_def = "\nDEFENSE:   " + str(int(user["def"]))
    t_eva = "\nEVASION:   " + str(int(user["eva"] * 100)) + "%"
    t_pre = "\nPRECISION: " + str(int(user["pre"] * 100)) + "%"

    # Text4.2 lines.
    sec_stats = " SEC. STATS:"
    t_str = "\n\n STRENGTH:   " + str(int(user["b_str"]))
    t_res = "\n RESISTANCE: " + str(int(user["b_res"]))
    t_agi = "\n AGILITY:    " + str(int(user["b_agi"]))
    t_dex = "\n DEXTERITY:  " + str(int(user["b_dex"]))
    t_vit = "\n VITALITY:   " + str(int(user["b_vit"]))

    text1 = t_loc + t_reg + t_coord + t_time + "\n." * 3
    text2 = des
    text3 = t_name + t_lvl + t_expbar + t_hp + t_hpbar + "\n." + t_gold
    text41 = prim_stats + t_atk + t_def + t_eva + t_pre
    text42 = sec_stats + t_str + t_res + t_agi + t_dex + t_vit
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
        if status:
            text5 += "\n" + DIRECTIONS[i]
    text5 += t_item1 + t_item2

    cmp_text = cmp_text + text_2_col(text5, text6, width, "|")
    cmp_text = cmp_text + text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "-")

    # cmp_text = concatenate_lists(cmp_text, side_text)
    patron = patron_print(globals.PATRON, len(cmp_text))

    for i, line in enumerate(cmp_text):
        print(" " + patron[i] + line + "  " + patron[i])


# Show inventory display.
def disp_show_inventory(inv: dict):
    items = [(item, quantity) for item, quantity in inv.items() if item not in ["walk", "permission", "message"] and not inv[item] <= 0]
    text = "INVENTORY:"
    for item, quantity in items:
        text += "\n - " + item.replace("_", " ").title() + ": " + str(quantity)
    return text


# Sleep options display.
def disp_sleep(x: int, y: int, set_map: dict) -> str:
    if "bed" in set_map[str((x, y))]["items"]:
        return "You want to sleep to:\n- Sleep to Morning\n- Sleep to Afternoon\n- Sleep to Evening\n- Sleep to Nigth"
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
