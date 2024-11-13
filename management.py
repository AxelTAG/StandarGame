# Imports.
# Local imports.
from actions import battle, talk
from globals import ENTRIES, MOBS
from map import Map
from player import Player
from utils import export_dict_to_txt, get_hash, export_player, export_settings

# External imports.
from datetime import datetime


# Event handler.
def event_handler(player: Player,
                  map_game: Map,
                  time_init: datetime) -> tuple[int, int]:
    # Event of Goblin Chief (1/3).
    if player.place == ENTRIES["sub_cave_2_2"] and not player.events["goblin_chief_crown"]:
        talk(npc=map_game.npcs["goblin griznuk"], player=player, map_game=map_game)

        play, menu, win = battle(player=player, enemy=MOBS["goblin chief"], ms=map_game.map_settings)

        if win:
            player.events["goblin_chief_crown"] = True
            talk(npc=map_game.npcs["mayors daughter maisie"], player=player, map_game=map_game)
            map_game.npcs["mayors daughter maisie"].messages = {
                0: ["My father, the mayor, will want to thank you properly. Please, come back with me to the village.",
                    "Words cannot express my gratitude, but I hope our people can repay  your bravery."]}
        return play, menu

    # Event of Goblin Chief (2/3).
    if (player.last_place == map_game.map_settings["(9, 4)"] and player.events["goblin_chief_crown"]
            and not player.events["message_maisie"]):
        ENTRIES["sub_cave_2_2"].npc = []
        map_game.map_settings["(10, 4)"].npc = ["mayor thorian", "mayors daughter maisie"]
        map_game.npcs["mayors daughter maisie"].messages = {
            0: ["Thank you, brave one!",
                "If not for your help, I might have tried to escape through one of the hidden passages in the cave.",
                "I saw them but had no chance to explore. Your courage saved me before I could take the risk.",
                "I owe you my life."]}
        map_game.npcs["mayor thorian"].messages = {
            0: [
                "I’ve heard the tale from my daughter, Maisie. You rescued her from the clutches of those vile goblins.",
                "I thank you, not as a mayor, but as a father. Our village owes you a debt we cannot repay.",
                "Please, accept this reward—a small token of our gratitude. Epiiat's doors are always open to you,"
                " brave soul."]}
        map_game.npcs["villager merrin"].messages = {
            0: ["You did it! You brought Maisie back safely. I can’t thank you enough.",
                "The whole village has been in distress since she went missing. You’ve given us hope again, brave one.",
                "We’ll not forget what you’ve done for Epiiat."]}
        map_game.npcs["villager fira"].messages = {
            0: ["I just heard the news—Maisie is safe and back home. What a blessing for the whole village.",
                "We’ve all been on edge since she went missing. It feels like a dark cloud has finally "
                "lifted from Epiiat."]}
        map_game.npcs["mayor thorian"].reset_hist_messages()

        player.inventory.add_item(item="hardened_leather_armor", quantity=1)
        player.events["message_maisie"] = True

    # Event of Goblin Chief (3/3).
    if player.events["message_maisie"] and map_game.npcs["mayor thorian"].hist_messages[0]:
        map_game.npcs["mayor thorian"].messages = {
            0: ["It’s rare to find such selfless bravery in these dark times. Thanks to you, my daughter is "
                "safe, and Epiiat breathes easier tonight.",
                "I must ensure the village knows of this deed; tales of courage like this must be remembered.",
                "May the gods guide that your steps, wherever the road may lead."]}

    # Event of Guard Lorian and Fisherman Marlin. The message. First part (1/2).
    if map_game.npcs["fisherman marlin"].hist_messages[0]:
        map_game.npcs["guard lorian"].messages = {
            0: ["Halt, traveler! Hyrule City permits only those with proper credentials to pass these gates.",
                "State your business and present your identification, or you shall not venture beyond.",
                "The safety of our citizens is paramount, and we cannot afford to be lax in these trying times."],
            1: ["Well, that old sea dog never forgets his family. Very well, you may pass. Tell him to visit when his "
                "fishing tales become too much for the villagers.",
                "Safe travels, adventurer."]}
        map_game.npcs["guard lorian"].answers = {
            1: "I have a message"}

        player.events["message"] = True

        return True, False

    # Event of Guard Lorian and Fisherman Marlin. The message. Second part (2/2).
    if player.events["message"] and map_game.npcs["guard lorian"].hist_messages[1]:
        map_game.npcs["guard lorian"].messages = {
            0: ["You've gained entry, but heed this counsel: Beyond the western outskirts lies uncharted territories"
                " and lurking dangers.",
                "Arm yourself well, noble traveler. The path is treacherous, and a sturdy sword or enchanted bow may"
                " be your greatest allies.",
                "Antina City rests in relative peace, but the world beyond is unpredictable. Safe travels, and may "
                "your blade remain sharp against the shadows that may encroach upon your journey."]}
        map_game.npcs["guard lorian"].reset_hist_messages()

        player.events["permission"] = True

        return True, False

    # Event batle with Dragon FireFrost after winning.
    if map_game.npcs["dragon firefrost"].hist_messages[0]:
        play, menu, win = battle(player=player, enemy=MOBS["dragon"].copy(), ms=map_game.map_settings)
        if win:
            map_game.npcs["dragon firefrost"].message = [
                "Impressive. Today, the winds of fate favor you.",
                "I yield. But heed my words, for when the stars align in a different cosmic dance, I shall await you"
                " once more.",
                "Until then, let the echoes of our encounter linger in the mountain breeze."
                " Farewell, " + player.name + ".",
                "Until our destinies entwine again."],

            talk(npc=map_game.npcs["dragon firefrost"], player=player, map_game=map_game)

            map_game.map_settings["(11, 24)"].description = ("Frozen valley, a pristine, snow-covered expanse where "
                                                             "frost-kissed silence reigns. Glistening ice formations "
                                                             "adorn the landscape, creating an ethereal and serene "
                                                             "winter tableau in nature's icy embrace.")
            map_game.map_settings["(11, 24)"].npc = []
            map_game.map_settings["(0, 0)"].entries["hut"].items.append("origami_flowers")
            map_game.npcs["dragon firefrost"] = [[], [], [], [0]]

            return play, menu
        else:
            map_game.npcs["dragon firefrost"].reset_hist_messages()
            save(player=player, map_game=map_game, time_init=time_init)
            return play, menu

    return True, False


# Load game function.
def load_game(path_usavepkl: str = "cfg_save.pkl", path_msave: str = "cfg_map.txt",
              path_settingpkl: str = "cfg_setting.pkl", path_hsave: str = "cfg_hash.txt"):
    pass


# Save function.
def save(player: Player,
         map_game: Map,
         time_init: datetime,
         path_usavepkl: str = "cfg_save.pkl",
         path_mappkl: str = "cfg_map.pkl",
         path_hsave: str = "cfg_hash.txt") -> None:
    player.refresh_time_played(datetime.now(), time_init)

    # Inventory, user stats and map setting saving (export to txt).
    export_player(player, path_usavepkl)
    export_player(map_game, path_mappkl)

    # Hash saving (export to dict).
    export_dict_to_txt(dictionary={"hash": get_hash(path_usavepkl)}, file_path=path_hsave)
