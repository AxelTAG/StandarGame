# Imports.
import globals
from utils import day_est, typewriter, clear, text_ljust
from displays import disp_title
import random


# Move function.
def move(
        x: int, y: int, map_heigt: int, map_width: int, inventory: dict,
        tl_map: list, mv: str) -> tuple[str, int, int, int]:
    hs = 8
    # Move North.
    if y > 0 and all(req in [*inventory.keys()] for req in globals.BIOMS[tl_map[y - 1][x]]["r"]) and mv == "1":
        if (tl_map[y - 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y - 1][x] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y - 1][x] in ["town", "gates"]):
            return "You moved North.", x, y - 1, hs
    # Move East.
    if x < map_heigt and all(req in [*inventory.keys()] for req in globals.BIOMS[tl_map[y][x + 1]]["r"]) and mv == "2":
        if (tl_map[y][x + 1] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y][x + 1] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y][x + 1] in ["town", "gates"]):
            return "You moved East.", x + 1, y, hs

    # Move South.
    if y < map_width and all(req in [*inventory.keys()] for req in globals.BIOMS[tl_map[y + 1][x]]["r"]) and mv == "3":
        if (tl_map[y + 1][x] == "town" and tl_map[y][x] in ["gates", "town"]) or (tl_map[y + 1][x] != "town" and tl_map[y][x] != "town") or (tl_map[y][x] == "town" and tl_map[y + 1][x] in ["town", "gates"]):
            return "You moved South.", x, y + 1, hs

    # Move West.
    if x > 0 and all(req in [*inventory.keys()] for req in globals.BIOMS[tl_map[y][x - 1]]["r"]) and mv == "4":
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


# Use boat.
def use_boat(x: int, y: int, inventory: dict, set_map: dict) -> tuple[str, dict, dict]:
    try:
        if "boat" in set_map[str((x, y))]["items"] and "boat" not in inventory.keys():
            inventory["boat"] = True
            del inventory["walk"]
            set_map[str((x, y))]["items"].remove("boat")
            set_map[str((x, y))]["d"] = "Seaside with swaying palm trees, echoing waves, and vibrant life."
            return "You are in the boat", inventory, set_map
        else:
            return "There is no boat here.", inventory, set_map
    except KeyError:
        return "There is no boat here.", inventory, set_map


# Land.
def land(x: int, y: int, inventory: dict, set_map: dict, tl_map: list) -> tuple[str, dict, dict]:
    if "boat" in inventory.keys() and tl_map[y][x] not in ["sea", "river"]:
        inventory["walk"] = True
        del inventory["boat"]
        set_map[str((x, y))]["items"].append("boat")
        set_map[str((x, y))]["d"] = "Seaside with anchored boat, echoing waves and vibrant coastal life."
        return "You have land.", inventory, set_map
    else:
        return "You can't land here.", inventory, set_map


# Talk.
def talk(npc: list, msg: list[str], quest: list[list] = None, res: list[str] = None) -> None:
    clear()
    for line in msg:
        clear()
        disp_title()
        print(" < GAME >")
        print()
        print(" " * 4 + " ".join(npc).title() + ":", end="\n ")
        print()
        lines = text_ljust(line, width=70)
        for text in lines:
            typewriter(" " * 4 + text)
            print()

        input(" " * 4 + "> ")


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


# Enter action.
def enter(x: int, y: int, entrie: str):
    if entrie == "cave":
        if (x, y) == (13, 0):
            if random.randint(1, 100) <= 50:
                return "You have crossed the cave without any problems.", 19, 0, False
            else:
                return "You have crossed the cave.", 19, 0, True

        if (x, y) == (19, 0):
            if random.randint(1, 100) <= 50:
                return "You have crossed the cave without any problems.", 13, 0, False
            else:
                return "You have crossed the cave.", 13, 0, True
    else:
        return "There is not a " + entrie + " here.", x, y, False


# Explore action.
def explore(x: int, y: int, inventory: dict, set_map: dict, tl_map: list) -> tuple[str, dict, dict]:
    pass
