# Imports.
# Local imports.
from biome import Entry
from globals import ENTRIES


# INIT MAP SETTING function that initialized the settings of map biomes.
def init_map_setting(ms: dict):
    # (0, 0)
    ms[(0, 0)].description = ("Solitary hut amidst lush foliage, surrounded by the symphony of waves and "
                              "the serenity of untouched nature.")
    ms[(0, 0)].entries = {"hut": ENTRIES["hut_0_0"]}
    ms[(0, 0)].entries["hut"].leave_entry = ms[(0, 0)]
    ms[(0, 0)].fight = False
    ms[(0, 0)].name = "ISLAND"

    # (1, 23)
    ms[(1, 13)].description = ("Rolling highlands with windswept grass, a sturdy artisan’s cabin billowing smoke from "
                               "its forge, and a tall stone tower overlooking the vast horizon.")
    ms[(1, 13)].name = "HIGHLANDS"
    ms[(1, 13)].entries = {"artisan_shop": ENTRIES["artisan_shop"]}
    ms[(1, 13)].entries["artisan_shop"].leave_entry = ms[(1, 13)]

    # (1, 23)
    ms[(1, 23)].description = ("Isolated shelter amid dangers, where rustling leaves and distant howls "
                               "suggest that safety within is uncertain at best.")
    ms[(1, 23)].entries = {"hut": ENTRIES["hut_1_23"]}
    ms[(1, 23)].entries["hut"].leave_entry = ms[(1, 23)]

    # (2, 0)
    ms[(2, 0)].mobs = ["litle slime", "slime", "poisonous slime"]
    ms[(2, 0)].mobs_chances = [5, 30, 50]

    # (2, 1)
    ms[(2, 1)].description = "Seaside with anchored boat, echoing waves and vibrant coastal life."
    ms[(2, 1)].items = ["boat"]

    # (2, 12)
    ms[(2, 12)].description = ("Rolling highlands with windswept grass, a sturdy artisan’s cabin billowing smoke from "
                               "its forge, and a tall stone tower overlooking the vast horizon.")
    ms[(2, 12)].name = "HIGHLANDS"
    ms[(2, 12)].entries = {"tower": ENTRIES["tower_of_karun_floor_1"]}
    ms[(2, 12)].entries["tower"].leave_entry = ms[(2, 12)]
    ms[(2, 12)].entries["tower"].entries = {"second_floor": ENTRIES["tower_of_karun_floor_2"]}

    # (5, 3)
    ms[(5, 3)].description = "Seaside with anchored boat, echoing waves and vibrant coastal life. A solitary" \
                             " figure stands at the water's edge, gazing out into the vastness of the sea, " \
                             "captivated by the rhythmic dance of the waves and the boundless horizon " \
                             "stretching before them."
    ms[(5, 3)].items = ["boat"]

    # (9, 4)
    ms[(9, 4)].description = ("Northern village entrance, sturdy gates open to a cozy haven, framed by "
                              "rolling hills and welcoming cottages.")
    ms[(9, 4)].name = "NORTHERN GATES"

    # (9, 5)
    ms[(9, 5)].description = ("Inn district, cozy tavern, lively marketplace, and quaint cottages "
                              "surround the inviting town.")
    ms[(9, 5)].entries = {"inn": ENTRIES["mirabelles_inn"],
                          "small_house": ENTRIES["house_epiiat_small"],
                          "house": ENTRIES["house_epiiat_normal"]}
    ms[(9, 5)].entries["inn"].leave_entry = ms[(9, 5)]
    ms[(9, 5)].entries["inn"].entries = {"main_room": ENTRIES["mirabelles_main_room"],
                                         "small_room": ENTRIES["mirabelles_small_room"]}
    ms[(9, 5)].entries["inn"].entries["main_room"].leave_entry = ms[(9, 5)].entries["inn"]
    ms[(9, 5)].entries["inn"].entries["small_room"].leave_entry = ms[(9, 5)].entries["inn"]
    ms[(9, 5)].entries["small_house"].leave_entry = ms[(9, 5)]
    ms[(9, 5)].entries["house"].leave_entry = ms[(9, 5)]

    # (9, 17)
    ms[(9, 17)].description = ("Eastern gateway to Antina: Mighty arches frame the welcoming path, guiding"
                               " travelers through a bustling thoroughfare toward the heart of the "
                               "enchanting city.")
    ms[(9, 17)].name = "EASTERN GATES"

    # (10, 4)
    ms[(10, 4)].description = "Village hub, Mayor's office, bustling square, and a quaint temple create the " \
                              "heart of community life."
    ms[(10, 4)].name = "TOWN CENTER"
    ms[(10, 4)].entries = {"mayors_house": ENTRIES["house_epiiat_mayor"],
                           "wooden_house": ENTRIES["house_epiiat_wooden"],
                           "temple": ENTRIES["temple_epiiat"]}
    ms[(10, 4)].entries["mayors_house"].leave_entry = ms[(10, 4)]
    ms[(10, 4)].entries["wooden_house"].leave_entry = ms[(10, 4)]
    ms[(10, 4)].entries["temple"].leave_entry = ms[(10, 4)]

    # (10, 5)
    ms[(10, 5)].description = ("Southern gateway, welcoming gates, cobblestone paths, and a charming,"
                               " serene atmosphere greet visitors.")
    ms[(10, 5)].name = "SOUTHERN GATES"

    # (10, 16)
    ms[(10, 16)].description = ("Majestic spires pierce the sky, casting a divine aura over cobblestone"
                                " squares. The sacred structure beckons pilgrims and whispers tales of"
                                " ancient reverence")
    ms[(10, 16)].name = "ANTINA'S SANCTUARY"
    ms[(10, 16)].entries = {"temple": ENTRIES["temple_antina"]}
    ms[(10, 16)].entries["temple"].leave_entry = ms[(10, 16)]

    # (10, 17)
    ms[(10, 17)].name = "ANTINA CITY"
    ms[(10, 17)].description = "Antina's post-gate district, winding streets lead to residential quarters " \
                               "and training grounds. Stone structures bear the weight of history, weaving a" \
                               " tapestry of everyday life beyond the bustling entrance gates."
    ms[(10, 17)].entries = {"potion_shop": ENTRIES["potion_shop_antina"]}
    ms[(10, 17)].entries["potion_shop"].leave_entry = ms[(10, 17)]

    # (10, 18)
    ms[(10, 18)].description = "Cobbled lanes weave among lively taverns and cozy inns, offering weary " \
                               "travelers respite. A symphony of laughter, music, and clinking tankards fills" \
                               " the air, creating an inviting atmosphere."
    ms[(10, 18)].entries = {"tavern": ENTRIES["the_golden_tankard_tavern"]}
    ms[(10, 18)].entries["tavern"].leave_entry = ms[(10, 18)]
    ms[(10, 18)].name = "ANTINA'S TAVERN DISTRICT"

    # (11, 15)
    ms[(11, 15)].description = "Antina's castle precinct, towering fortress crowned with turrets dominates " \
                               "the cityscape. Home to nobility and adorned with banners, the castle " \
                               "overlooks sprawling courtyards, embodying the seat of power in Antina."
    ms[(11, 15)].entries = {"castle": ENTRIES["castle"]}
    ms[(11, 15)].entries["castle"].leave_entry = ms[(11, 15)]
    ms[(11, 15)].name = "ANTINA'S CASTLE"

    # (11, 16)
    ms[(11, 16)].description = "A grand centerpiece adorned with intricate sculptures, where cascading waters" \
                               " mirror the city's vibrancy, inviting residents and visitors to linger in its" \
                               " refreshing ambiance."
    ms[(11, 16)].name = "ANTINA'S FOUNTAIN SQUARE"

    # (11, 17)
    ms[(11, 17)].description = "Antina's medieval hub, majestic castle towers overlook bustling market " \
                               "squares, where knights, merchants, and mystics converge. Cobblestone streets " \
                               "wind through diverse districts, echoing with the city's vibrant heartbeat."
    ms[(11, 17)].name = "ANTINA'S MARKET"

    # (11, 18)
    ms[(11, 18)].description = "Quaint abodes line tranquil streets, adorned with blooming gardens. A serene" \
                               " enclave where the city's heartbeat echoes in the everyday rhythms of its" \
                               " residents."
    ms[(11, 18)].entries = {"mid_house": ENTRIES["house_antina_gareth"],
                            "small_house": ENTRIES["house_antina_small"],
                            "white_house": ENTRIES["house_antina_white"],
                            "family_house": ENTRIES["house_antina_family"]}
    ms[(11, 18)].entries["mid_house"].leave_entry = ms[(11, 18)]
    ms[(11, 18)].entries["small_house"].leave_entry = ms[(11, 18)]
    ms[(11, 18)].entries["white_house"].leave_entry = ms[(11, 18)]
    ms[(11, 18)].entries["family_house"].leave_entry = ms[(11, 18)]
    ms[(11, 18)].name = "ANTINA'S RESIDENTIAL QUARTER"

    # (11, 24)
    ms[(11, 24)].description = "Frozen valley under the watchful gaze of a dragon, crystalized landscapes " \
                               "echo with the dragon's silent vigil, as icy winds and shimmering frost create" \
                               " an otherworldly ambiance."
    ms[(11, 24)].name = "FROSTVALE"

    # (12, 16)
    ms[(12, 16)].description = "Quaint abodes line tranquil streets, adorned with blooming gardens. A serene" \
                               " enclave where the city's heartbeat echoes in the everyday rhythms of its " \
                               "residents."
    ms[(12, 16)].name = "ANTINA'S RESIDENTIAL QUARTER"
    ms[(12, 16)].entries = {"edrions_house": ENTRIES["house_antina_edrion"],
                            "arics_house": ENTRIES["house_antina_aric"]}

    # (12, 17)
    ms[(12, 17)].description = "Antina's post-gate district, winding streets lead to residential quarters and" \
                               " training grounds. Stone structures bear the weight of history, weaving a " \
                               "tapestry of everyday life beyond the bustling entrance gates."
    ms[(12, 17)].name = "ANTINA CITY"

    # (12, 18)
    ms[(12, 18)].description = ("Antina's arena district: Colossal stone coliseum stands amidst cheering"
                                " crowds. Brave warriors clash within, seeking glory and honor, while"
                                " merchants peddle wares to the fervent spectators, creating an "
                                "electrifying atmosphere.")
    ms[(12, 18)].name = "ANTINA'S ARENA"
    ms[(12, 18)].entries = {"arena": ENTRIES["arena_antina"]}
    ms[(12, 18)].entries["arena"].leave_entry = ms[(12, 18)]

    # (13, 0)
    ms[(13, 0)].description = "Rugged terrain, sinister caves, and sneaky goblin tribes dominate these " \
                              "perilous elevated lands."
    ms[(13, 0)].mobs = ["goblin"]
    ms[(13, 0)].mobs_chances = [40]
    ms[(13, 0)].name = "HIGHLANDS"

    # (13, 0): Cave - stage 0
    cave_13_0 = ENTRIES["cave_13_0"]
    cave_13_0.leave_entry = ms[(13, 0)]
    ms[(13, 0)].entries = {"cave_entrance": cave_13_0}

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
    sub_cave_4_0.leave_entry = ms[(19, 0)]

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
                            "surface": ms[(19, 0)]}

    # (13, 17)
    ms[(13, 17)].name = "EAST GATES"
    ms[(13, 17)].description = "Eastern city-state entrance: Towering gates adorned with intricate carvings," \
                               " guarded by vigilant sentinels, mark the grand entry to a thriving metropolis" \
                               " blending history and modernity."

    # (14, 5)
    ms[(14, 5)].description = "Blocked valley passage, boulders from a recent landslide obstruct the way, as " \
                              "a diligent worker clears debris, striving to reopen this vital route amidst " \
                              "the rugged beauty of the scenic landscape."
    ms[(14, 5)].name = "VALLEY"

    # (15, 5)
    ms[(15, 5)].req = ["rocks"]

    # (19, 0)
    ms[(19, 0)].description = "Rugged terrain, sinister caves, and sneaky goblin tribes dominate these " \
                              "perilous elevated lands."
    ms[(19, 0)].entries = {"cave_entrance": ENTRIES["sub_cave_4_0"]}

    # (22, 1)
    ms[(22, 1)].description = "Abandoned woodland hut, dilapidated and forgotten, this rustic abode near the" \
                              " forest stands as a silent witness to nature's reclamation."
    ms[(22, 1)].name = "DARK FOREST"

    # (22, 18)
    first_floor = ENTRIES["tower_of_eldra_floor_1"]
    first_floor.leave_entry = ms[(22, 18)]

    second_floor = ENTRIES["tower_of_eldra_floor_2"]
    second_floor.leave_entry = first_floor

    ms[(22, 18)].description = ("Vast, rocky expanse crowned with a solitary wooden tower. The structure "
                                "stands tall, offering sweeping views of the sky and distant horizons.")
    ms[(22, 18)].name = "PLATEAU"
    ms[(22, 18)].entries = {"tower_of_eldra": first_floor}
    ms[(22, 18)].entries["tower_of_eldra"].entries = {"tower_of_eldra_second_floor": second_floor}

    # (22, 27)
    ms[(22, 27)].description = ("Sandy shores meet grassy dunes, where a weathered hut stands, surrounded"
                                " by scattered driftwood and the soothing sound of crashing waves.")
    ms[(22, 27)].name = "COAST"
    ms[(22, 27)].entries = {"coast_hut": ENTRIES["hut_22_27"]}
    ms[(22, 27)].entries["coast_hut"].leave_entry = ms[(22, 27)]

    # (26, 15)
    ms[(26, 15)].description = "Aquiri's portside entrance: Bustling harbor welcomes ships with salty " \
                               "breezes. Weathered docks and colorful boats set the scene for a lively " \
                               "maritime haven in this coastal village."
    ms[(26, 15)].name = "AQUIRI'S PORTSIDE ENTRANCE"

    # (27, 14)
    ms[(27, 14)].description = "Seaside fishing hamlet, colorful boats bob gently in the harbor, while " \
                               "weathered cottages line the shore of this picturesque coastal community. A " \
                               "lone fisherman casts his net into the glistening waters, capturing the " \
                               "essence of maritime tranquility."
    ms[(27, 14)].name = "AQUIRI'S VILLAGE"
    ms[(27, 14)].entries = {"marlins_hut": ENTRIES["house_aquiri_marlin"],
                            "house": ENTRIES["house_aquiri_normal"]}
    ms[(27, 14)].entries["marlins_hut"].leave_entry = ms[(27, 14)]
    ms[(27, 14)].entries["house"].leave_entry = ms[(27, 14)]

    # (27, 15)
    ms[(27, 15)].description = "Seaside fishing hamlet, colorful boats bob gently in the harbor, while " \
                               "weathered cottages line the shore of this picturesque coastal community."
    ms[(27, 15)].entries = {
        "inn": ENTRIES["lyssias_inn"],
        "coast_stone_house": ENTRIES["house_aquiri_stone"],
        "thornes_ship": ENTRIES["thornes_ship"]}

    ms[(27, 15)].entries["inn"].leave_entry = ms[(27, 15)]
    ms[(27, 15)].entries["coast_stone_house"].leave_entry = ms[(27, 15)]
    ms[(27, 15)].entries["thornes_ship"].leave_entry = ms[(27, 15)]

    ms[(27, 15)].entries["inn"].entries = {
        "first_room": ENTRIES["lyssias_first_room"],
        "second_room": ENTRIES["lyssias_second_room"],
        "third_room": ENTRIES["lyssias_third_room"]}
    ms[(27, 15)].entries["inn"].entries["first_room"].leave_entry = ms[(27, 15)].entries["inn"]
    ms[(27, 15)].entries["inn"].entries["second_room"].leave_entry = ms[(27, 15)].entries["inn"]
    ms[(27, 15)].entries["inn"].entries["third_room"].leave_entry = ms[(27, 15)].entries["inn"]
    ms[(27, 15)].name = "AQUIRI'S VILLAGE"

    # (27, 15)
    ms[(27, 19)].entries = {
        "cave": ENTRIES["cave_27_19"]}
    ms[(27, 19)].entries["cave"].leave_entry = ms[(27, 19)]

    ms[(27, 19)].entries["cave"].entries = {
        "coast": ms[(27, 19)],
        "plateu": ms[(23, 18)]}
