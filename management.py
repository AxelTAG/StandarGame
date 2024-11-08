# Imports.
# Local imports.
from actions import battle, talk
from map import Map
from player import Player
from utils import export_dict_to_txt, get_hash, export_player, export_settings

# External imports.
from datetime import datetime


# Event handler.
def event_handler(player: Player,
                  map_game: Map,
                  npc: dict,
                  ms: dict,
                  mobs: dict,
                  time_init: datetime,
                  play: int,
                  menu: int) -> tuple[dict, dict, int, int]:

    # Event of Guard Lorian and Fisherman Marlin. The message. First part (1/2).
    if npc["fisherman marlin"].hist_messages[0]:
        npc["guard lorian"].messages = {
            0: ["Halt, traveler! Hyrule City permits only those with proper credentials to pass these gates.",
                "State your business and present your identification, or you shall not venture beyond.",
                "The safety of our citizens is paramount, and we cannot afford to be lax in these trying times."],
            1: ["Well, that old sea dog never forgets his family. Very well, you may pass. Tell him to visit when his "
                "fishing tales become too much for the villagers.",
                "Safe travels, adventurer."]}
        npc["guard lorian"].answers = {
            1: "I have a message"}

        player.events["message"] = True

        return npc, ms, play, menu

    # Event of Guard Lorian and Fisherman Marlin. The message. Second part (2/2).
    elif player.events["message"] and npc["guard lorian"].hist_messages[1]:
        npc["guard lorian"].messages = {
            0: ["You've gained entry, but heed this counsel: Beyond the western outskirts lies uncharted territories"
                 " and lurking dangers.",
                 "Arm yourself well, noble traveler. The path is treacherous, and a sturdy sword or enchanted bow may"
                 " be your greatest allies.",
                 "Antina City rests in relative peace, but the world beyond is unpredictable. Safe travels, and may "
                 "your blade remain sharp against the shadows that may encroach upon your journey."]}
        npc["guard lorian"].reset_hist_messages()

        player.events["permission"] = True

        return npc, ms, play, menu

    # Event batle with Dragon FireFrost after winning.
    elif npc["dragon firefrost"].hist_messages[0]:
        play, menu, win = battle(player, mobs["dragon"].copy(), ms)
        if win:
            npc["dragon firefrost"].message = ["Impressive. Today, the winds of fate favor you.",
                                               "I yield. But heed my words, for when the stars align in a different "
                                               "cosmic dance, I shall await you once more.",
                                               "Until then, let the echoes of our encounter linger in the mountain "
                                               "breeze. Farewell, " + player.name + ".",
                                               "Until our destinies entwine again."],

            talk(npc=npc["dragon firefrost"], player=player, map_game=map_game)

            ms["(11, 24)"].description = "Frozen valley, a pristine, snow-covered expanse where frost-kissed silence" \
                                         " reigns. Glistening ice formations adorn the landscape, creating an " \
                                         "ethereal and serene winter tableau in nature's icy embrace."
            ms["(11, 24)"].npc = []
            ms["(0, 0)"].entries["hut"].items.append("origami_flowers")
            npc["dragon firefrost"] = [[], [], [], [0]]

            return npc, ms, play, menu
        else:
            npc["dragon firefrost"].reset_hist_messages()
            save(player, npc, ms, time_init)
            return npc, ms, play, menu

    else:
        return npc, ms, play, menu


# Load game function.
def load_game(path_usavepkl: str = "cfg_save.pkl", path_msave: str = "cfg_map.txt",
              path_settingpkl: str = "cfg_setting.pkl", path_hsave: str = "cfg_hash.txt"):
    pass


# Save function.
def save(player: Player,
         map_game: Map,
         npc: dict,
         time_init: datetime,
         path_usavepkl: str = "cfg_save.pkl",
         path_mappkl: str = "cfg_map.pkl",
         path_settingpkl: str = "cfg_setting.pkl",
         path_hsave: str = "cfg_hash.txt") -> None:

    player.refresh_time_played(datetime.now(), time_init)

    # Inventory, user stats and map setting saving (export to txt).
    export_player(player, path_usavepkl)
    export_player(map_game, path_mappkl)
    export_settings({"npc": npc}, path_settingpkl)

    # Hash saving (export to dict).
    export_dict_to_txt({"hash": get_hash(path_usavepkl)}, path_hsave)
