# Imports.
# Local imports.
from biome import Entry
from globals import ENTRIES
from utils import coordstr


# INIT MAP SETTING function that initialized the settings of map biomes.
def init_map_setting(ms: dict):
    # (0, 0)
    ms[coordstr(x=0, y=0)].description = ("Solitary hut amidst lush foliage, surrounded by the symphony of waves and "
                                          "the serenity of untouched nature.")
    ms[coordstr(x=0, y=0)].entries = {"hut": ENTRIES["hut_0_0"]}
    ms[coordstr(x=0, y=0)].entries["hut"].leave_entry = ms[coordstr(x=0, y=0)]
    ms[coordstr(x=0, y=0)].fight = False
    ms[coordstr(x=0, y=0)].name = "ISLAND"

    # (1, 23)
    ms[coordstr(x=1, y=23)].description = ("Isolated shelter amid dangers, where rustling leaves and distant howls "
                                           "suggest that safety within is uncertain at best.")
    ms[coordstr(x=1, y=23)].entries = {"hut": ENTRIES["hut_1_23"]}
    ms[coordstr(x=1, y=23)].entries["hut"].leave_entry = ms[coordstr(x=1, y=23)]

    # (2, 0)
    ms[coordstr(x=2, y=0)].mobs = ["litle slime", "slime", "poisonous slime"]
    ms[coordstr(x=2, y=0)].mobs_chances = [5, 30, 50]

    # (2, 1)
    ms[coordstr(x=2, y=1)].description = "Seaside with anchored boat, echoing waves and vibrant coastal life."
    ms[coordstr(x=2, y=1)].items = ["boat"]

    # (5, 3)
    ms[coordstr(x=5,
                y=3)].description = "Seaside with anchored boat, echoing waves and vibrant coastal life. A solitary" \
                                    " figure stands at the water's edge, gazing out into the vastness of the sea, " \
                                    "captivated by the rhythmic dance of the waves and the boundless horizon " \
                                    "stretching before them."
    ms[coordstr(x=5, y=3)].items = ["boat"]
    ms[coordstr(x=5, y=3)].npc = ["captain zelian"]

    # (9, 4)
    ms[coordstr(x=9, y=4)].description = ("Northern village entrance, sturdy gates open to a cozy haven, framed by "
                                          "rolling hills and welcoming cottages.")
    ms[coordstr(x=9, y=4)].name = "NORTHERN GATES"
    ms[coordstr(x=9, y=4)].npc = ["traveler thaldir"]

    # (9, 5)
    ms[coordstr(x=9, y=5)].description = ("Inn district, cozy tavern, lively marketplace, and quaint cottages "
                                          "surround the inviting town.")
    ms[coordstr(x=9, y=5)].entries = {"inn": ENTRIES["mirabelles_inn"]}
    ms[coordstr(x=9, y=5)].entries["inn"].leave_entry = ms[coordstr(x=9, y=5)]
    ms[coordstr(x=9, y=5)].entries["inn"].entries = {"main_room": ENTRIES["mirabelles_main_room"],
                                                     "small_room": ENTRIES["mirabelles_small_room"]}
    ms[coordstr(x=9, y=5)].entries["inn"].entries["main_room"].leave_entry = ms[coordstr(x=9, y=5)].entries["inn"]
    ms[coordstr(x=9, y=5)].entries["inn"].entries["small_room"].leave_entry = ms[coordstr(x=9, y=5)].entries["inn"]
    ms[coordstr(x=9, y=5)].npc = ["merchant bryson", "traveler sylas", "villager merrin", "traveler renan"]

    # (9, 17)
    ms[coordstr(x=9, y=17)].description = ("Eastern gateway to Antina: Mighty arches frame the welcoming path, guiding"
                                           " travelers through a bustling thoroughfare toward the heart of the "
                                           "enchanting city.")
    ms[coordstr(x=9, y=17)].name = "EASTERN GATES"
    ms[coordstr(x=9, y=17)].npc = ["traveler kaelin"]

    # (10, 4)
    ms[coordstr(x=10,
                y=4)].description = "Village hub, Mayor's office, bustling square, and a quaint temple create the " \
                                    "heart of community life."
    ms[coordstr(x=10, y=4)].name = "TOWN CENTER"
    ms[coordstr(x=10, y=4)].npc = ["mayor thorian"]

    # (10, 5)
    ms[coordstr(x=10, y=5)].description = ("Southern gateway, welcoming gates, cobblestone paths, and a charming,"
                                           " serene atmosphere greet visitors.")
    ms[coordstr(x=10, y=5)].name = "SOUTHERN GATES"
    ms[coordstr(x=10, y=5)].npc = ["traveler elara", "villager fira"]

    # (10, 16)
    ms[coordstr(x=10, y=16)].description = ("Majestic spires pierce the sky, casting a divine aura over cobblestone"
                                            " squares. The sacred structure beckons pilgrims and whispers tales of"
                                            " ancient reverence")
    ms[coordstr(x=10, y=16)].name = "ANTINA'S CATHEDRAL"
    ms[coordstr(x=10, y=16)].entries = {"cathedral": Entry(
        color=ms[coordstr(x=10, y=16)].color,
        description="Cathedral interior, stained glass bathes the solemn space in kaleidoscopic hues. Ornate pillars,"
                    " echoing arches, and the hushed reverence create an awe-inspiring sanctuary of divine grandeur.")}
    ms[coordstr(x=10, y=16)].entries["cathedral"].leave_entry = ms[coordstr(x=10, y=16)]

    # (10, 17)
    ms[coordstr(x=10, y=17)].name = "ANTINA CITY"
    ms[coordstr(x=10, y=17)].description = "Antina's post-gate district, winding streets lead to residential quarters " \
                                           "and training grounds. Stone structures bear the weight of history, weaving a" \
                                           " tapestry of everyday life beyond the bustling entrance gates."

    # (10, 18)
    ms[coordstr(x=10, y=18)].description = "Cobbled lanes weave among lively taverns and cozy inns, offering weary " \
                                           "travelers respite. A symphony of laughter, music, and clinking tankards fills" \
                                           " the air, creating an inviting atmosphere."
    ms[coordstr(x=10, y=18)].entries = {"tavern": Entry(
        color=ms[coordstr(x=10, y=18)].color,
        description="Bustling tavern, clinking mugs, and lively chatter. Cozy nooks, plush furnishings, and a hearth"
                    " invite urban travelers to unwind in this vibrant, communal haven.",
        items=["bed"],
        name="TAVERN")}
    ms[coordstr(x=10, y=18)].entries["tavern"].leave_entry = ms[coordstr(x=10, y=18)]
    ms[coordstr(x=10, y=18)].name = "ANTINA'S TAVERN DISTRICT"

    # (11, 15)
    ms[coordstr(x=11, y=15)].description = "Antina's castle precinct, towering fortress crowned with turrets dominates " \
                                           "the cityscape. Home to nobility and adorned with banners, the castle " \
                                           "overlooks sprawling courtyards, embodying the seat of power in Antina."
    ms[coordstr(x=11, y=15)].entries = {"castle": Entry(
        color=ms[coordstr(x=11, y=15)].color,
        description="Bustling tavern, clinking mugs, and lively chatter. Cozy nooks, plush furnishings, and a hearth"
                    " invite urban travelers to unwind in this vibrant, communal haven.",
        name="CASTLE SALOON",
        npc=["lord aric"])}
    ms[coordstr(x=11, y=15)].entries["castle"].leave_entry = ms[coordstr(x=11, y=15)]
    ms[coordstr(x=11, y=15)].name = "ANTINA'S CASTLE"

    # (11, 16)
    ms[coordstr(x=11,
                y=16)].description = "A grand centerpiece adorned with intricate sculptures, where cascading waters" \
                                     " mirror the city's vibrancy, inviting residents and visitors to linger in its" \
                                     " refreshing ambiance."
    ms[coordstr(x=11, y=16)].name = "ANTINA'S FOUNTAIN SQUARE"

    # (11, 17)
    ms[coordstr(x=11, y=17)].description = "Antina's medieval hub, majestic castle towers overlook bustling market " \
                                           "squares, where knights, merchants, and mystics converge. Cobblestone streets " \
                                           "wind through diverse districts, echoing with the city's vibrant heartbeat."
    ms[coordstr(x=11, y=17)].name = "ANTINA'S MARKET"
    ms[coordstr(x=11, y=17)].npc = ["merchant roland"]

    # (11, 18)
    ms[coordstr(x=11,
                y=18)].description = "Quaint abodes line tranquil streets, adorned with blooming gardens. A serene" \
                                     " enclave where the city's heartbeat echoes in the everyday rhythms of its" \
                                     " residents."
    ms[coordstr(x=11, y=18)].name = "ANTINA'S RESIDENTIAL QUARTER"

    # (11, 24)
    ms[coordstr(x=11, y=18)].description = "Frozen valley under the watchful gaze of a dragon, crystalized landscapes " \
                                           "echo with the dragon's silent vigil, as icy winds and shimmering frost create" \
                                           " an otherworldly ambiance."
    ms[coordstr(x=11, y=24)].name = "FROSTVALE"
    ms[coordstr(x=11, y=24)].npc = ["dragon firefrost"]

    # (12, 16)
    ms[coordstr(x=12,
                y=16)].description = "Quaint abodes line tranquil streets, adorned with blooming gardens. A serene" \
                                     " enclave where the city's heartbeat echoes in the everyday rhythms of its " \
                                     "residents."
    ms[coordstr(x=12, y=16)].name = "ANTINA'S RESIDENTIAL QUARTER"

    # (12, 17)
    ms[coordstr(x=12,
                y=17)].description = "Antina's post-gate district, winding streets lead to residential quarters and" \
                                     " training grounds. Stone structures bear the weight of history, weaving a " \
                                     "tapestry of everyday life beyond the bustling entrance gates."
    ms[coordstr(x=12, y=17)].name = "ANTINA CITY"
    ms[coordstr(x=12, y=17)].req = ["permission"]

    # (12, 18)
    ms[coordstr(x=12, y=18)].description = ("Antina's arena district: Colossal stone coliseum stands amidst cheering"
                                            " crowds. Brave warriors clash within, seeking glory and honor, while"
                                            " merchants peddle wares to the fervent spectators, creating an "
                                            "electrifying atmosphere.")
    ms[coordstr(x=12, y=18)].name = "ANTINA'S ARENA"
    ms[coordstr(x=12, y=18)].npc = ["merchant elden"]

    # (13, 0)
    ms[coordstr(x=13, y=0)].description = "Rugged terrain, sinister caves, and sneaky goblin tribes dominate these " \
                                          "perilous elevated lands."
    ms[coordstr(x=13, y=0)].mobs = ["goblin"]
    ms[coordstr(x=13, y=0)].mobs_chances = [40]
    ms[coordstr(x=13, y=0)].name = "HIGHLANDS"

    # (13, 0): Cave - stage 0
    cave_13_0 = ENTRIES["cave_13_0"]
    cave_13_0.leave_entry = ms[coordstr(x=13, y=0)]
    ms[coordstr(x=13, y=0)].entries = {"cave_entrance": cave_13_0}

    # (13, 0): Cave - stage 1
    sub_cave_1_0 = ENTRIES["sub_cave_1_0"]
    sub_cave_1_1 = ENTRIES["sub_cave_1_1"]
    sub_cave_1_2 = ENTRIES["sub_cave_1_2"]

    cave_13_0.entries = {"cave_pit": sub_cave_1_0,
                         "hole": sub_cave_1_1,
                         "big_cave": sub_cave_1_2}

    # (13, 0): Cave - stage 2
    sub_cave_2_0 = ENTRIES["sub_cave_2_0"]
    sub_cave_2_1 = ENTRIES["sub_cave_2_1"]
    sub_cave_2_2 = ENTRIES["sub_cave_2_2"]
    sub_cave_2_3 = ENTRIES["sub_cave_2_3"]
    sub_cave_2_4 = ENTRIES["sub_cave_2_4"]

    sub_cave_1_0.entries = {"cave_entrance": cave_13_0,
                            "cave_basin": sub_cave_2_0}
    sub_cave_1_1.entries = {"cave_entrance": cave_13_0}
    sub_cave_1_2.entries = {"cave_entrance": cave_13_0,
                            "passageway_cave_entrance": sub_cave_2_3,
                            "cave_chamber": sub_cave_2_4}

    # (13, 0): Cave - stage 3
    sub_cave_3_0 = ENTRIES["sub_cave_3_0"]
    sub_cave_3_1 = ENTRIES["sub_cave_3_1"]
    sub_cave_3_2 = ENTRIES["sub_cave_3_2"]

    sub_cave_2_0.entries = {"cave_pit": sub_cave_1_0,
                            "cave_gallery": sub_cave_3_0}
    sub_cave_2_1.entries = {"goblin_chief_bedroom": sub_cave_2_2,
                            "cave_gallery": sub_cave_3_0}
    sub_cave_2_2.entries = {"chiefs_cave": sub_cave_2_1}
    sub_cave_2_2.npc = ["mayors daughter maisie"]
    
    sub_cave_2_3.entries = {"big_cave": sub_cave_1_2,
                            "cave_passageway_exit": sub_cave_3_1,
                            "goblin_dining_gallery": sub_cave_3_2}
    sub_cave_2_4.entries = {"big_cave": sub_cave_1_2}

    # (13, 0): Cave - stage 4
    sub_cave_4_0 = ENTRIES["sub_cave_4_0"]
    sub_cave_4_0.leave_entry = ms[coordstr(x=19, y=0)]

    sub_cave_3_0.entries = {"cave_basin": sub_cave_2_0,
                            "chiefs_cave": sub_cave_2_1,
                            "cave_passageway_exit": sub_cave_3_1}
    sub_cave_3_1.entries = {"chimney": sub_cave_4_0,
                            "cave_gallery": sub_cave_3_0,
                            "goblin_dining_gallery": sub_cave_3_2,
                            "cave_passageway_entrance": sub_cave_2_3}
    sub_cave_3_2.entries = {"cave_passageway_entrance": sub_cave_2_3,
                            "goblin_dining_gallery": sub_cave_3_2}
    sub_cave_4_0.entries = {"cave_passageway_exit": sub_cave_3_1,
                            "surface": ms[coordstr(x=19, y=0)]}

    # (13, 17)
    ms[coordstr(x=13, y=17)].name = "EAST GATES"
    ms[coordstr(x=13,
                y=17)].description = "Eastern city-state entrance: Towering gates adorned with intricate carvings," \
                                     " guarded by vigilant sentinels, mark the grand entry to a thriving metropolis" \
                                     " blending history and modernity."
    ms[coordstr(x=13, y=17)].npc = ["guard lorian", "traveler elinor"]

    # (14, 5)
    ms[coordstr(x=14,
                y=5)].description = "Blocked valley passage, boulders from a recent landslide obstruct the way, as " \
                                    "a diligent worker clears debris, striving to reopen this vital route amidst " \
                                    "the rugged beauty of the scenic landscape."
    ms[coordstr(x=14, y=5)].name = "VALLEY"
    ms[coordstr(x=14, y=5)].npc = ["worker gorrick", "traveler seraph"]

    # (15, 5)
    ms[coordstr(x=15, y=5)].description = "Nothing important here."
    ms[coordstr(x=15, y=5)].name = "ROCKS"
    ms[coordstr(x=15, y=5)].req = ["wings"]

    # (19, 0)
    ms[coordstr(x=19, y=0)].description = "Rugged terrain, sinister caves, and sneaky goblin tribes dominate these " \
                                          "perilous elevated lands."
    ms[coordstr(x=19, y=0)].entries = {"cave_entrance": ENTRIES["sub_cave_4_0"]}

    # (22, 1)
    ms[coordstr(x=22,
                y=1)].description = "Abandoned woodland hut, dilapidated and forgotten, this rustic abode near the" \
                                    " forest stands as a silent witness to nature's reclamation."
    ms[coordstr(x=22, y=1)].name = "DARK FOREST"

    # (22, 18)
    first_floor = ENTRIES["tower_of_eldra_floor_1"]
    first_floor.leave_entry = ms[coordstr(x=22, y=18)]

    second_floor = ENTRIES["tower_of_eldra_floor_2"]
    second_floor.leave_entry = first_floor

    ms[coordstr(x=22, y=18)].description = ("Vast, rocky expanse crowned with a solitary wooden tower. The structure "
                                            "stands tall, offering sweeping views of the sky and distant horizons.")
    ms[coordstr(x=22, y=18)].name = "PLATEAU"
    ms[coordstr(x=22, y=18)].entries = {"tower_of_eldra": first_floor}
    ms[coordstr(x=22, y=18)].entries["tower_of_eldra"].entries = {"tower_of_eldra_second_floor": second_floor}

    # (22, 27)
    ms[coordstr(x=18, y=24)].description = ("Seaside hut, weathered wood and a thatched roof, filled with fishing "
                                            "gear and seashells. The salty breeze drifts through, mingling with the "
                                            "scent of dried fish.")
    ms[coordstr(x=18, y=24)].name = "PLAINS"
    ms[coordstr(x=18, y=24)].npc = ["fisherman brann"]

    # (26, 15)
    ms[coordstr(x=26, y=15)].description = "Aquiri's portside entrance: Bustling harbor welcomes ships with salty " \
                                           "breezes. Weathered docks and colorful boats set the scene for a lively " \
                                           "maritime haven in this coastal village."
    ms[coordstr(x=26, y=15)].name = "AQUIRI'S PORTSIDE ENTRANCE"

    # (27, 14)
    ms[coordstr(x=27, y=14)].description = "Seaside fishing hamlet, colorful boats bob gently in the harbor, while " \
                                           "weathered cottages line the shore of this picturesque coastal community. A " \
                                           "lone fisherman casts his net into the glistening waters, capturing the " \
                                           "essence of maritime tranquility."
    ms[coordstr(x=27, y=14)].name = "AQUIRI'S VILLAGE"
    ms[coordstr(x=27, y=14)].npc = ["fisherman marlin"]

    # (27, 15)
    ms[coordstr(x=27, y=15)].description = "Seaside fishing hamlet, colorful boats bob gently in the harbor, while " \
                                           "weathered cottages line the shore of this picturesque coastal community."
    ms[coordstr(x=27, y=15)].entries = {"inn": Entry(
        items=["bed"])}
    ms[coordstr(x=27, y=15)].entries["inn"].leave_entry = ms[coordstr(27, 15)]
    ms[coordstr(x=27, y=15)].name = "AQUIRI'S VILLAGE"
    ms[coordstr(x=27, y=15)].npc = ["captain thorne", "merchant selena"]
