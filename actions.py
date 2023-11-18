# Imports.
import globals
from utils import day_est


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


# Sleep in bed.
def sleep_in_bed(x: int, y: int, set_map: dict, hp, hpmax, actual_hs, opt: str) -> tuple[str, int, int, str]:
    if opt not in ["morning", "afternoon", "evening", "night"]:
        hs, d_moment = day_est(actual_hs, 0)
        return ".", hp, hs, d_moment
    else:
        if "bed" in set_map[(x, y)][0]:
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
        if "boat" in set_map[(x, y)][0] and "boat" not in inventory.keys():
            inventory["boat"] = True
            del inventory["walk"]
            set_map[(x, y)][0].remove("boat")
            set_map[(x, y)][1] = "Seaside with swaying palm trees, echoing waves, and vibrant life."
            return "You are in the boat", inventory, set_map
        else:
            return "There is no boat here.", inventory, set_map
    except KeyError:
        return "There is no boat here.", inventory, set_map


# Land.
def land(x: int, y: int, inventory: dict, set_map: dict, tl_map: list) -> tuple[str, dict, dict]:
    try:
        if "boat" in inventory.keys() and tl_map[x][y] not in ["sea", "river"]:
            inventory["walk"] = True
            del inventory["boat"]
            set_map[(x, y)][0].append("boat")
            set_map[(x, y)][1] = "Seaside with anchored boat, echoing waves and vibrant coastal life."
            return "You have land.", inventory, set_map
        else:
            return "You can't land here.", inventory, set_map
    except KeyError:
        return "You can't land here.", inventory, set_map
