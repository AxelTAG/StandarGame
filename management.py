# Imports.
# External imports.
import numpy as np

# Local imports.
from actions import battle, talk
from inventory import Inventory
from player import Player
from utils import export_dict_to_txt, get_hash, export_player


# Save function.
def save(player, user_map: np.array, npc: dict, ms: dict, path_usavepkl: str = "cfg_save.pkl",
         path_msave: str = "cfg_map.txt", path_usave: str = "cfg_save.txt", path_hsave: str = "cfg_hash.txt") -> None:

    # Map drawing of user saving (export to txt).
    np.savetxt(path_msave, user_map.reshape(-1, user_map.shape[-1]), fmt='%d', delimiter='\t')

    # Inventory, user stats and map setting saving (export to txt).
    export_player(player, path_usavepkl)
    export_dict_to_txt({2: npc, 9: ms}, path_usave)

    # Hash saving (export to dict).
    export_dict_to_txt({"hash": get_hash(path_usavepkl)}, path_hsave)


# Event handler.
def event_handler(player: Player(), user_map: np.array, npc: dict, ms: dict, mobs: dict,
                  play: int, menu: int) -> tuple[dict, dict, int, int]:
    if npc["fisherman marlin"][3][0] and not npc["guard lorian"][3][1]:
        npc["guard lorian"] = [["Halt, traveler! Hyrule City permits only those with proper credentials to pass these "
                                "gates.", "State your business and present your identification, or you shall not "
                                "venture beyond.", "The safety of our citizens is paramount, and we cannot afford to be "
                                "lax in these trying times."],
                               [["I have a message", ["Marlin, you say?", "Well, that old "
                                "sea dog never forgets his family. Very well, you may pass. Tell him to visit when his "
                                "fishing tales become too much for the villagers.", "Safe travels, adventurer."]],
                                ["Leave", ["..."]]],
                               [], [0, 0, 0]]

        return npc, ms, play, menu

    elif npc["guard lorian"][3][1] and not player.events["message"]:
        npc["guard lorian"] = [["You've gained entry, but heed this counsel: Beyond the western outskirts lies "
                                "uncharted territories and lurking dangers.", "Arm yourself well, noble traveler. The "
                                "path is treacherous, and a sturdy sword or enchanted bow may be your greatest allies.",
                                "Antina City rests in relative peace, but the world beyond is unpredictable. "
                                "Safe travels, and may your blade remain sharp against the shadows that may encroach "
                                "upon your journey."], [], [], [0, True, 0]]
        player.events["message"] = True
        player.events["permission"] = True

        ms["(12, 17)"]["r"].remove("permission")

        return npc, ms, play, menu

    elif npc["dragon firefrost"][3][0]:
        play, menu, win = battle(player, mobs["dragon"].copy(), ms)
        if win:
            npc["dragon firefrost"] = [["Impressive. Today, the winds of fate favor you.", "I yield. But heed my words,"
                                        " for when the stars align in a different cosmic dance, I shall await you "
                                        "once more.", "Until then, let the echoes of our encounter linger in the "
                                        "mountain breeze. Farewell, " + player.name + ".", "Until our destinies "
                                         "entwine again."],
                                       [], [], [0]]
            talk(npc=npc["dragon firefrost"], npc_name="dragon firefrost", player=player)
            ms["(11, 24)"]["d"] = "Frozen valley, a pristine, snow-covered expanse where frost-kissed silence reigns." \
                                  " Glistening ice formations adorn the landscape, creating an ethereal and " \
                                  "serene winter tableau in nature's icy embrace."
            ms["(11, 24)"]["npc"] = []
            ms["(0, 0)"]["items"].append("origami flowers")
            npc["dragon firefrost"] = [[], [], [], [0]]
            return npc, ms, play, menu
        else:
            npc["dragon firefrost"][3] = [0]
            save(player, user_map, npc, ms)
            return npc, ms, play, menu

    else:
        return npc, ms, play, menu
