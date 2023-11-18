# Imports.
from utils import text_2_col

# Constants.
DIRECTIONS = {0: "1 - NORTH",  1: "2 - EAST", 2: "3 - SOUTH", 3: "4 - WEST"}


# Bar display
def disp_bar(n: int = 18, disp: bool = True) -> str:
    text = "--" + "-" * n + "--"
    if disp:
        print(text)
    return text


# Play display.
def disp_play(
        loc: str, reg: str, time: str, des: str, name: str, hp: int, hpmax: int, lvl: int, exp: int, expmax: int,
        atk: int, item1: int, item2: int, gold: int, x: int, y: int, mdir: list, faction: list, screen_text: str,
        width: int) -> None:
    t_loc = "LOCATION: " + loc.upper()
    t_reg = "\n REGION: " + reg.upper()
    t_coord = "\n COORD: " + str(x) + " " + str(y)
    t_time = "\n TIME OF DAY: " + time.upper()
    t_name = "NAME: " + name.upper()
    t_hp = "\n HP: " + str(hp) + "/" + str(hpmax)
    t_lvl = "\n LVL: " + str(lvl) + "  -  EXP: " + str(exp) + "/" + str(expmax)
    t_atk = "\n ATK: " + str(atk)
    t_item1 = "\n POTIONS: " + str(item1)
    t_item2 = "\n ELIXIRS: " + str(item2)
    t_gold = "\n GOLD: " + str(gold)

    text1 = t_loc + t_reg + t_coord + t_time + "\n." * 3
    text2 = des
    text3 = t_name + t_hp + t_lvl + t_atk + t_item1 + t_item2 + t_gold
    text4 = "."
    text5 = "0 - SAVE AND QUIT"
    text6 = screen_text

    for line in text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "+"):
        print(" " + line)

    for line in text_2_col(text1, text2, width, "|"):
        print(" " + line)

    for line in text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "+"):
        print(" " + line)

    for line in text_2_col(text3, text4, width, "|"):
        print(" " + line)

    for line in text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "+"):
        print(" " + line)

    for i, status in enumerate(mdir):
        if status:
            text5 += "\n" + DIRECTIONS[i]

    for line in text_2_col(text5, text6, width, "|"):
        print(" " + line)

    for line in text_2_col(disp_bar(width - 4, disp=False), disp_bar(width - 4, disp=False), width, "+"):
        print(" " + line)


# Sleep options display.
def disp_sleep(x: int, y: int, set_map: dict) -> str:
    if "bed" in set_map[(x, y)][0]:
        return "You want to sleep to:\n- Sleep to Morning\n- Sleep to Afternoon\n- Sleep to Evening\n- Sleep to Nigth"
    else:
        return "There is no bed here."
