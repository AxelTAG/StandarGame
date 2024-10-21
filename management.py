# Imports.
# Local imports.
from actions import battle, talk
from biome import Biome, Entry
from npc import Npc
from player import Player
from utils import coordstr, export_dict_to_txt, get_hash, export_player, export_settings

# External imports.
import numpy as np
from datetime import datetime


# Event handler.
def event_handler(player: Player,
                  npc: dict,
                  ms: dict,
                  mobs: dict,
                  time_init: datetime,
                  play: int,
                  menu: int) -> tuple[dict, dict, int, int]:

    # Event of Guard Lorian and Fisherman Marlin. The message. First part.
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

    # Event of Guard Lorian and Fisherman Marlin. The message. Second part.
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

            talk(npc=npc["dragon firefrost"], player=player)

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


# INIT MAP SETTING function that initialized the settings of map biomes.
def init_map_setting(ms: dict):
    # (0, 0)
    ms[coordstr(0, 0)].description = "Solitary hut amidst lush foliage, surrounded by the symphony of waves and the" \
                               " serenity of untouched nature."
    ms[coordstr(0, 0)].entries = {"hut": Entry(
        color=ms[coordstr(0, 0)].color,
        description="Island hut, a cozy retreat adorned with a bed, a table, two "
                    "chairs, and a window, invites serenity amid nature's whispers.",
        items=["bed", "short_sword"])}
    ms[coordstr(0, 0)].entries["hut"].leave_entry = ms[coordstr(0, 0)]
    ms[coordstr(0, 0)].fight = False
    ms[coordstr(0, 0)].name = "ISLAND"

    # (1, 23)
    ms[coordstr(1, 23)].description = "Isolated shelter amid dangers, where rustling leaves and distant howls suggest" \
                                      " that safety within is uncertain at best."
    ms[coordstr(1, 23)].entries = {"hut": Entry(
        color=ms[coordstr(1, 23)].color,
        description="Interior of isolated refuge, dimly lit, flickering candles cast dancing shadows on weathered "
                    "walls. Tattered maps and makeshift barricades hint at cautious attempts to secure the uncertain"
                    " safety within.",
        items=["bed"])}
    ms[coordstr(1, 23)].entries["hut"].leave_entry = ms[coordstr(1, 23)]

    # (2, 0)
    ms[coordstr(2, 0)].mobs = ["litle slime", "slime", "poisonous slime"]
    ms[coordstr(2, 0)].mobs_chances = [5, 30, 50]

    # (2, 1)
    ms[coordstr(2, 1)].description = "Seaside with anchored boat, echoing waves and vibrant coastal life."
    ms[coordstr(2, 1)].items = ["boat"]

    # (5, 3)
    ms[coordstr(5, 3)].description = "Seaside with anchored boat, echoing waves and vibrant coastal life. A solitary" \
                                     " figure stands at the water's edge, gazing out into the vastness of the sea, " \
                                     "captivated by the rhythmic dance of the waves and the boundless horizon " \
                                     "stretching before them."
    ms[coordstr(5, 3)].items = ["boat"]
    ms[coordstr(5, 3)].npc = ["captain zelian"]

    # (9, 4)
    ms[coordstr(9, 4)].description = "Northern village entrance, sturdy gates open to a cozy haven, framed by rolling" \
                                     " hills and welcoming cottages."
    ms[coordstr(9, 4)].name = "NORTHERN GATES"
    ms[coordstr(9, 4)].npc = ["traveler thaldir"]

    # (9, 5)
    ms[coordstr(9, 5)].description = "Inn district, cozy tavern, lively marketplace, and quaint cottages surround " \
                                     "the inviting town."
    ms[coordstr(9, 5)].entries = {"inn": Entry(
        color=ms[coordstr(9, 5)].color,
        description="Warm hearth, wooden beams, and cozy furnishings create a welcoming atmosphere. Aromas of "
                    "home-cooked meals linger, inviting weary travelers to find respite.",
        entries={
            "main_room": Entry(
                color=ms[coordstr(9, 5)].color,
                description="In the main chamber of the inn, a comfortable bed awaits amidst the charming ambiance of "
                            "a warm hearth, rustic wooden beams, and snug furnishings.",
                items=["bed"],
                name="MIRABELLE'S INN MAIN ROOM",
                req=["main_room_key"]),
            "small_room": Entry(
                color=ms[coordstr(9, 5)].color,
                description="In the main chamber of the inn, a comfortable bed awaits amidst the charming ambiance of "
                            "a warm hearth, rustic wooden beams, and snug furnishings.",
                items=["bed"],
                name="MIRABELLE'S INN SMALL ROOM",
                req=["small_room_key"])},
        name="MIRABELLE'S INN",
        npc=["innkeeper mirabelle"])}

    ms[coordstr(9, 5)].entries["inn"].leave_entry = ms[coordstr(9, 5)]
    ms[coordstr(9, 5)].entries["inn"].entries["main_room"].leave_entry = ms[coordstr(9, 5)].entries["inn"]
    ms[coordstr(9, 5)].entries["inn"].entries["small_room"].leave_entry = ms[coordstr(9, 5)].entries["inn"]
    ms[coordstr(9, 5)].npc = ["merchant bryson", "traveler sylas"]

    # (9, 17)
    ms[coordstr(9, 17)].description = "Eastern gateway to Antina: Mighty arches frame the welcoming path, guiding " \
                                      "travelers through a bustling thoroughfare toward the heart of the enchanting " \
                                      "city."
    ms[coordstr(9, 17)].name = "EASTERN GATES"
    ms[coordstr(9, 17)].npc = ["traveler kaelin"]

    # (10, 4)
    ms[coordstr(10, 4)].description = "Village hub, Mayor's office, bustling square, and a quaint temple create the " \
                                      "heart of community life."
    ms[coordstr(10, 4)].name = "TOWN CENTER"
    ms[coordstr(10, 4)].npc = ["mayor thorian"]

    # (10, 5)
    ms[coordstr(10, 5)].description = "Southern gateway, welcoming gates, cobblestone paths, and a charming, serene" \
                                      " atmosphere greet visitors."
    ms[coordstr(10, 5)].name = "SOUTHERN GATES"
    ms[coordstr(10, 5)].npc = ["traveler elara"]

    # (10, 16)
    ms[coordstr(10, 16)].description = "Majestic spires pierce the sky, casting a divine aura over cobblestone " \
                                       "squares. The sacred structure beckons pilgrims and whispers tales of ancient" \
                                       " reverence"
    ms[coordstr(10, 16)].name = "ANTINA'S CATHEDRAL"
    ms[coordstr(10, 16)].entries = {"cathedral": Entry(
        color=ms[coordstr(10, 16)].color,
        description="Cathedral interior, stained glass bathes the solemn space in kaleidoscopic hues. Ornate pillars,"
                    " echoing arches, and the hushed reverence create an awe-inspiring sanctuary of divine grandeur.")}
    ms[coordstr(10, 16)].entries["cathedral"].leave_entry = ms[coordstr(10, 16)]

    # (10, 17)
    ms[coordstr(10, 17)].name = "ANTINA CITY"
    ms[coordstr(10, 17)].description = "Antina's post-gate district, winding streets lead to residential quarters " \
                                       "and training grounds. Stone structures bear the weight of history, weaving a" \
                                       " tapestry of everyday life beyond the bustling entrance gates."

    # (10, 18)
    ms[coordstr(10, 18)].description = "Cobbled lanes weave among lively taverns and cozy inns, offering weary " \
                                       "travelers respite. A symphony of laughter, music, and clinking tankards fills" \
                                       " the air, creating an inviting atmosphere."
    ms[coordstr(10, 18)].entries = {"tavern": Entry(
        color=ms[coordstr(10, 18)].color,
        description="Bustling tavern, clinking mugs, and lively chatter. Cozy nooks, plush furnishings, and a hearth"
                    " invite urban travelers to unwind in this vibrant, communal haven.",
        items=["bed"],
        name="TAVERN")}
    ms[coordstr(10, 18)].entries["tavern"].leave_entry = ms[coordstr(10, 18)]
    ms[coordstr(10, 18)].name = "ANTINA'S TAVERN DISTRICT"

    # (11, 15)
    ms[coordstr(11, 15)].description = "Antina's castle precinct, towering fortress crowned with turrets dominates " \
                                       "the cityscape. Home to nobility and adorned with banners, the castle " \
                                       "overlooks sprawling courtyards, embodying the seat of power in Antina."
    ms[coordstr(11, 15)].entries = {"castle": Entry(
        color=ms[coordstr(11, 15)].color,
        description="Bustling tavern, clinking mugs, and lively chatter. Cozy nooks, plush furnishings, and a hearth"
                    " invite urban travelers to unwind in this vibrant, communal haven.",
        name="CASTLE SALOON",
        npc=["lord aric"])}
    ms[coordstr(11, 15)].entries["castle"].leave_entry = ms[coordstr(11, 15)]
    ms[coordstr(11, 15)].name = "ANTINA'S CASTLE"

    # (11, 16)
    ms[coordstr(11, 16)].description = "A grand centerpiece adorned with intricate sculptures, where cascading waters" \
                                       " mirror the city's vibrancy, inviting residents and visitors to linger in its" \
                                       " refreshing ambiance."
    ms[coordstr(11, 16)].name = "ANTINA'S FOUNTAIN SQUARE"

    # (11, 17)
    ms[coordstr(11, 17)].description = "Antina's medieval hub, majestic castle towers overlook bustling market " \
                                       "squares, where knights, merchants, and mystics converge. Cobblestone streets " \
                                       "wind through diverse districts, echoing with the city's vibrant heartbeat."
    ms[coordstr(11, 17)].name = "ANTINA'S MARKET"
    ms[coordstr(11, 17)].npc = ["merchant roland"]

    # (11, 18)
    ms[coordstr(11, 18)].description = "Quaint abodes line tranquil streets, adorned with blooming gardens. A serene" \
                                       " enclave where the city's heartbeat echoes in the everyday rhythms of its" \
                                       " residents."
    ms[coordstr(11, 18)].name = "ANTINA'S RESIDENTIAL QUARTER"

    # (11, 24)
    ms[coordstr(11, 18)].description = "Frozen valley under the watchful gaze of a dragon, crystalized landscapes " \
                                       "echo with the dragon's silent vigil, as icy winds and shimmering frost create" \
                                       " an otherworldly ambiance."
    ms[coordstr(11, 24)].name = "FROSTVALE"
    ms[coordstr(11, 24)].npc = ["dragon firefrost"]

    # (12, 16)
    ms[coordstr(12, 16)].description = "Quaint abodes line tranquil streets, adorned with blooming gardens. A serene" \
                                       " enclave where the city's heartbeat echoes in the everyday rhythms of its " \
                                       "residents."
    ms[coordstr(12, 16)].name = "ANTINA'S RESIDENTIAL QUARTER"

    # (12, 17)
    ms[coordstr(12, 17)].description = "Antina's post-gate district, winding streets lead to residential quarters and" \
                                       " training grounds. Stone structures bear the weight of history, weaving a " \
                                       "tapestry of everyday life beyond the bustling entrance gates."
    ms[coordstr(12, 17)].name = "ANTINA CITY"
    ms[coordstr(12, 17)].req = ["permission"]

    # (12, 18)
    ms[coordstr(12, 18)].description = "Antina's arena district: Colossal stone coliseum stands amidst cheering " \
                                       "crowds. Brave warriors clash within, seeking glory and honor, while merchants" \
                                       " peddle wares to the fervent spectators, creating an electrifying atmosphere."
    ms[coordstr(12, 18)].name = "ANTINA'S ARENA"
    ms[coordstr(12, 18)].npc = ["merchant elden"]

    # (13, 0)
    ms[coordstr(13, 0)].description = "Rugged terrain, sinister caves, and sneaky goblin tribes dominate these " \
                                      "perilous elevated lands."
    ms[coordstr(13, 0)].mobs = ["goblin", "orc"]
    ms[coordstr(13, 0)].mobs_chances = [40, 90]
    ms[coordstr(13, 0)].name = "HIGHLANDS"

    # (13, 17)
    ms[coordstr(13, 17)].name = "EAST GATES"
    ms[coordstr(13, 17)].description = "Eastern city-state entrance: Towering gates adorned with intricate carvings," \
                                       " guarded by vigilant sentinels, mark the grand entry to a thriving metropolis" \
                                       " blending history and modernity."
    ms[coordstr(13, 17)].npc = ["guard lorian", "traveler elinor"]

    # (14, 5)
    ms[coordstr(14, 5)].description = "Blocked valley passage, boulders from a recent landslide obstruct the way, as " \
                                      "a diligent worker clears debris, striving to reopen this vital route amidst " \
                                      "the rugged beauty of the scenic landscape."
    ms[coordstr(14, 5)].name = "VALLEY"
    ms[coordstr(14, 5)].npc = ["worker gorrick", "traveler seraph"]

    # (15, 5)
    ms[coordstr(15, 5)].description = "Nothing important here."
    ms[coordstr(15, 5)].name = "ROCKS"
    ms[coordstr(15, 5)].req = ["wings"]

    # (18, 24)
    ms[coordstr(18, 24)].description = "Abandoned woodland hut, dilapidated and forgotten, this rustic abode near the" \
                                       " forest stands as a silent witness to nature's reclamation."
    ms[coordstr(18, 24)].name = "FOREST"

    # (19, 0)
    ms[coordstr(19, 0)].description = "Rugged terrain, sinister caves, and sneaky goblin tribes dominate these " \
                                      "perilous elevated lands."
    ms[coordstr(19, 0)].entries = ["cave"]

    # (22, 1)
    ms[coordstr(22, 1)].description = "Abandoned woodland hut, dilapidated and forgotten, this rustic abode near the" \
                                      " forest stands as a silent witness to nature's reclamation."
    ms[coordstr(22, 1)].name = "DARK FOREST"

    # (26, 15)
    ms[coordstr(26, 15)].description = "Aquiri's portside entrance: Bustling harbor welcomes ships with salty " \
                                       "breezes. Weathered docks and colorful boats set the scene for a lively " \
                                       "maritime haven in this coastal village."
    ms[coordstr(26, 15)].name = "AQUIRI'S PORTSIDE ENTRANCE"

    # (27, 14)
    ms[coordstr(27, 14)].description = "Seaside fishing hamlet, colorful boats bob gently in the harbor, while " \
                                       "weathered cottages line the shore of this picturesque coastal community. A " \
                                       "lone fisherman casts his net into the glistening waters, capturing the " \
                                       "essence of maritime tranquility."
    ms[coordstr(27, 14)].name = "AQUIRI'S VILLAGE"
    ms[coordstr(27, 14)].npc = ["fisherman marlin"]

    # (27, 15)
    ms[coordstr(27, 15)].description = "Seaside fishing hamlet, colorful boats bob gently in the harbor, while " \
                                       "weathered cottages line the shore of this picturesque coastal community."
    ms[coordstr(27, 15)].entries = {"inn": Entry(
        items=["bed"])}
    ms[coordstr(27, 15)].entries["inn"].leave_entry = ms[coordstr(27, 15)]
    ms[coordstr(27, 15)].name = "AQUIRI'S VILLAGE"
    ms[coordstr(27, 15)].npc = ["captain thorne", "merchant selena"]


# Load game function.
def load_game(path_usavepkl: str = "cfg_save.pkl", path_msave: str = "cfg_map.txt",
              path_settingpkl: str = "cfg_setting.pkl", path_hsave: str = "cfg_hash.txt"):
    pass


# Save function.
def save(player: Player,
         npc: dict,
         ms: dict, time_init: datetime,
         path_usavepkl: str = "cfg_save.pkl",
         path_settingpkl: str = "cfg_setting.pkl",
         path_hsave: str = "cfg_hash.txt") -> None:

    player.refresh_time_played(datetime.now(), time_init)

    # Inventory, user stats and map setting saving (export to txt).
    export_player(player, path_usavepkl)
    export_settings({"npc": npc, "ms": ms}, path_settingpkl)

    # Hash saving (export to dict).
    export_dict_to_txt({"hash": get_hash(path_usavepkl)}, path_hsave)
