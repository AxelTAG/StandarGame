# Imports.
# Local imports.
from world import ENTRIES


# INIT MAP SETTING function that initialized the settings of map biomes.
def init_map_setting(ms: dict):
    # (12, 24)
    ms[(12, 24)].description = ("Solitary hut amidst lush foliage, surrounded by the symphony of waves and "
                                "the serenity of untouched nature.")
    ms[(12, 24)].entries = {"hut": ENTRIES["hut_12_24"]}
    ms[(12, 24)].entries["hut"].leave_entry = ms[(12, 24)]
    ms[(12, 24)].fight = False
    ms[(12, 24)].name = "ISLAND"

    # (13, 37)
    ms[(13, 37)].description = ("Rolling highlands with windswept grass, a sturdy artisan’s cabin billowing smoke from "
                                "its forge, and a tall stone tower overlooking the vast horizon.")
    ms[(13, 37)].name = "HIGHLANDS"
    ms[(13, 37)].entries = {"artisan_shop": ENTRIES["artisan_shop"]}
    ms[(13, 37)].entries["artisan_shop"].leave_entry = ms[(13, 37)]

    # (13, 47)
    ms[(13, 47)].description = ("Isolated shelter amid dangers, where rustling leaves and distant howls "
                                "suggest that safety within is uncertain at best.")
    ms[(13, 47)].entries = {"hut": ENTRIES["hut_13_47"]}
    ms[(13, 47)].entries["hut"].leave_entry = ms[(13, 47)]

    # (14, 24)
    ms[(14, 24)].mobs = ["little slime", "slime"]
    ms[(14, 24)].mobs_chances = [20, 50]

    # (14, 25)
    ms[(14, 25)].description = ("Seaside with swaying palm trees, echoing waves, and vibrant life. "
                                "Anchored boat gently resting by the shore.")
    ms[(14, 25)].items = ["boat"]

    # (14, 36)
    ms[(14, 36)].description = ("Rolling highlands with windswept grass, a sturdy artisan’s cabin billowing smoke from "
                                "its forge, and a tall stone tower overlooking the vast horizon.")
    ms[(14, 36)].name = "HIGHLANDS"
    ms[(14, 36)].entries = {"tower": ENTRIES["tower_of_karun_floor_1"]}
    ms[(14, 36)].entries["tower"].leave_entry = ms[(14, 36)]
    ms[(14, 36)].entries["tower"].entries = {"second_floor": ENTRIES["tower_of_karun_floor_2"]}
    ms[(14, 36)].entries["tower"].entries["second_floor"].items = ["giant_telescope"]

    # (17, 27)
    ms[(17, 27)].description = "Seaside with swaying palm trees, echoing waves, and vibrant life. A solitary" \
                               " figure stands at the water's edge, gazing out into the vastness of the sea, " \
                               "captivated by the rhythmic dance of the waves and the boundless horizon " \
                               "stretching before them. Anchored boat gently resting by the shore."
    ms[(17, 27)].items = ["boat"]

    # (21, 28)
    ms[(21, 28)].description = ("Northern village entrance, sturdy gates open to a cozy haven, framed by "
                                "rolling hills and welcoming cottages.")
    ms[(21, 28)].name = "NORTHERN GATES"

    # (21, 29)
    ms[(21, 29)].description = ("Inn district, cozy tavern, lively marketplace, and quaint cottages "
                                "surround the inviting town.")
    ms[(21, 29)].entries = {"inn": ENTRIES["mirabelles_inn"],
                            "small_house": ENTRIES["house_epiiat_small"],
                            "house": ENTRIES["house_epiiat_normal"]}
    ms[(21, 29)].entries["inn"].leave_entry = ms[(21, 29)]
    ms[(21, 29)].entries["inn"].entries = {"main_room": ENTRIES["mirabelles_main_room"],
                                           "small_room": ENTRIES["mirabelles_small_room"]}
    ms[(21, 29)].entries["inn"].entries["main_room"].leave_entry = ms[(21, 29)].entries["inn"]
    ms[(21, 29)].entries["inn"].entries["small_room"].leave_entry = ms[(21, 29)].entries["inn"]
    ms[(21, 29)].entries["small_house"].leave_entry = ms[(21, 29)]
    ms[(21, 29)].entries["house"].leave_entry = ms[(21, 29)]

    # (21, 41)
    ms[(21, 41)].description = ("Eastern gateway to Antina: Mighty arches frame the welcoming path, guiding"
                                " travelers through a bustling thoroughfare toward the heart of the "
                                "enchanting city.")
    ms[(21, 41)].name = "EASTERN GATES"

    # (22, 28)
    ms[(22, 28)].description = "Village hub, Mayor's office, bustling square, and a quaint temple create the " \
                               "heart of community life."
    ms[(22, 28)].name = "TOWN CENTER"
    ms[(22, 28)].entries = {"mayors_house": ENTRIES["house_epiiat_mayor"],
                            "wooden_house": ENTRIES["house_epiiat_wooden"],
                            "temple": ENTRIES["temple_epiiat"]}
    ms[(22, 28)].entries["mayors_house"].leave_entry = ms[(22, 28)]
    ms[(22, 28)].entries["wooden_house"].leave_entry = ms[(22, 28)]
    ms[(22, 28)].entries["temple"].leave_entry = ms[(22, 28)]

    # (22, 29)
    ms[(22, 29)].description = ("Southern gateway, welcoming gates, cobblestone paths, and a charming,"
                                " serene atmosphere greet visitors.")
    ms[(22, 29)].name = "SOUTHERN GATES"

    # (22, 40)
    ms[(22, 40)].description = ("Majestic spires pierce the sky, casting a divine aura over cobblestone"
                                " squares. The sacred structure beckons pilgrims and whispers tales of"
                                " ancient reverence")
    ms[(22, 40)].name = "ANTINA'S SANCTUARY"
    ms[(22, 40)].entries = {"temple": ENTRIES["temple_antina"]}
    ms[(22, 40)].entries["temple"].leave_entry = ms[(22, 40)]

    # (22, 41)
    ms[(22, 41)].name = "ANTINA CITY"
    ms[(22, 41)].description = "Antina's post-gate district, winding streets lead to residential quarters " \
                               "and training grounds. Stone structures bear the weight of history, weaving a" \
                               " tapestry of everyday life beyond the bustling entrance gates."
    ms[(22, 41)].entries = {"potion_shop": ENTRIES["potion_shop_antina"]}
    ms[(22, 41)].entries["potion_shop"].leave_entry = ms[(22, 41)]

    # (22, 42)
    ms[(22, 42)].description = "Cobbled lanes weave among lively taverns and cozy inns, offering weary " \
                               "travelers respite. A symphony of laughter, music, and clinking tankards fills" \
                               " the air, creating an inviting atmosphere."
    ms[(22, 42)].entries = {"tavern": ENTRIES["the_golden_tankard_tavern"],
                            "inn": ENTRIES["aliras_inn"]}
    ms[(22, 42)].entries["tavern"].leave_entry = ms[(22, 42)]
    ms[(22, 42)].entries["inn"].leave_entry = ms[(22, 42)]
    ms[(22, 42)].entries["inn"].entries = {
        "first_room": ENTRIES["aliras_first_room"],
        "second_room": ENTRIES["aliras_second_room"],
        "third_room": ENTRIES["aliras_third_room"],
        "fourth_room": ENTRIES["aliras_fourth_room"]}
    ms[(22, 42)].entries["inn"].entries["first_room"].leave_entry = ms[(22, 42)].entries["inn"]
    ms[(22, 42)].entries["inn"].entries["second_room"].leave_entry = ms[(22, 42)].entries["inn"]
    ms[(22, 42)].entries["inn"].entries["third_room"].leave_entry = ms[(22, 42)].entries["inn"]
    ms[(22, 42)].entries["inn"].entries["fourth_room"].leave_entry = ms[(22, 42)].entries["inn"]

    ms[(22, 42)].name = "ANTINA'S TAVERN DISTRICT"

    # (23, 39)
    ms[(23, 39)].description = "Antina's castle precinct, towering fortress crowned with turrets dominates " \
                               "the cityscape. Home to nobility and adorned with banners, the castle " \
                               "overlooks sprawling courtyards, embodying the seat of power in Antina."
    ms[(23, 39)].entries = {"castle": ENTRIES["castle"]}
    ms[(23, 39)].entries["castle"].leave_entry = ms[(23, 39)]
    ms[(23, 39)].name = "ANTINA'S CASTLE"

    # (23, 40)
    ms[(23, 40)].description = "A grand centerpiece adorned with intricate sculptures, where cascading waters" \
                               " mirror the city's vibrancy, inviting residents and visitors to linger in its" \
                               " refreshing ambiance."
    ms[(23, 40)].name = "ANTINA'S FOUNTAIN SQUARE"

    # (23, 41)
    ms[(23, 41)].description = "Antina's medieval hub, majestic castle towers overlook bustling market " \
                               "squares, where knights, merchants, and mystics converge. Cobblestone streets " \
                               "wind through diverse districts, echoing with the city's vibrant heartbeat."
    ms[(23, 41)].name = "ANTINA'S MARKET"

    # (23, 42)
    ms[(23, 42)].description = "Quaint abodes line tranquil streets, adorned with blooming gardens. A serene" \
                               " enclave where the city's heartbeat echoes in the everyday rhythms of its" \
                               " residents."
    ms[(23, 42)].entries = {"mid_house": ENTRIES["house_antina_gareth"],
                            "small_house": ENTRIES["house_antina_small"],
                            "white_house": ENTRIES["house_antina_white"],
                            "family_house": ENTRIES["house_antina_family"]}
    ms[(23, 42)].entries["mid_house"].leave_entry = ms[(23, 42)]
    ms[(23, 42)].entries["small_house"].leave_entry = ms[(23, 42)]
    ms[(23, 42)].entries["white_house"].leave_entry = ms[(23, 42)]
    ms[(23, 42)].entries["family_house"].leave_entry = ms[(23, 42)]
    ms[(23, 42)].name = "ANTINA'S RESIDENTIAL QUARTER"

    # (23, 48)
    ms[(23, 48)].description = "Frozen valley under the watchful gaze of a dragon, crystalized landscapes " \
                               "echo with the dragon's silent vigil, as icy winds and shimmering frost create" \
                               " an otherworldly ambiance."
    ms[(23, 48)].name = "FROSTVALE"

    # (24, 40)
    ms[(24, 40)].description = "Quaint abodes line tranquil streets, adorned with blooming gardens. A serene" \
                               " enclave where the city's heartbeat echoes in the everyday rhythms of its " \
                               "residents."
    ms[(24, 40)].name = "ANTINA'S RESIDENTIAL QUARTER"
    ms[(24, 40)].entries = {"edrions_house": ENTRIES["house_antina_edrion"],
                            "arics_house": ENTRIES["house_antina_aric"]}

    # (24, 41)
    ms[(24, 41)].description = "Antina's post-gate district, winding streets lead to residential quarters and" \
                               " training grounds. Stone structures bear the weight of history, weaving a " \
                               "tapestry of everyday life beyond the bustling entrance gates."
    ms[(24, 41)].name = "ANTINA CITY"

    # (24, 42)
    ms[(24, 42)].description = ("Antina's arena district: Colossal stone coliseum stands amidst cheering"
                                " crowds. Brave warriors clash within, seeking glory and honor, while"
                                " merchants peddle wares to the fervent spectators, creating an "
                                "electrifying atmosphere.")
    ms[(24, 42)].name = "ANTINA'S ARENA"
    ms[(24, 42)].entries = {"arena": ENTRIES["arena_antina"]}
    ms[(24, 42)].entries["arena"].leave_entry = ms[(24, 42)]

    # (25, 24)
    ms[(25, 24)].description = "Rugged terrain, sinister caves, and sneaky goblin tribes dominate these " \
                               "perilous elevated lands."
    ms[(25, 24)].mobs = ["goblin"]
    ms[(25, 24)].mobs_chances = [40]
    ms[(25, 24)].name = "HIGHLANDS"

    # (25, 24): Cave - stage 0
    cave_13_0 = ENTRIES["cave_25_24"]
    cave_13_0.leave_entry = ms[(25, 24)]
    ms[(25, 24)].entries = {"cave_entrance": cave_13_0}

    # (25, 24): Cave - stage 1
    sub_cave_1_0 = ENTRIES["sub_cave_1_0"]
    sub_cave_1_1 = ENTRIES["sub_cave_1_1"]
    sub_cave_1_2 = ENTRIES["sub_cave_1_2"]

    cave_13_0.entries = {"cave_pit": sub_cave_1_0,
                         "hole": sub_cave_1_1,
                         "big_cave": sub_cave_1_2}

    # (25, 24): Cave - stage 2
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

    # (25, 24): Cave - stage 3
    sub_cave_3_0 = ENTRIES["sub_cave_3_0"]
    sub_cave_3_1 = ENTRIES["sub_cave_3_1"]
    sub_cave_3_2 = ENTRIES["sub_cave_3_2"]

    sub_cave_2_0.entries = {"cave_pit": sub_cave_1_0,
                            "cave_gallery": sub_cave_3_0}
    sub_cave_2_1.entries = {"goblin_chief_bedroom": sub_cave_2_2,
                            "cave_gallery": sub_cave_3_0}
    sub_cave_2_2.entries = {"chiefs_cave": sub_cave_2_1}

    sub_cave_2_3.entries = {"big_cave": sub_cave_1_2,
                            "cave_passageway_exit": sub_cave_3_1,
                            "goblin_dining_gallery": sub_cave_3_2}
    sub_cave_2_4.entries = {"big_cave": sub_cave_1_2}

    # (25, 24): Cave - stage 4
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
                            "cave_passageway_exit": sub_cave_3_1}
    sub_cave_4_0.entries = {"cave_passageway_exit": sub_cave_3_1,
                            "surface": ms[(31, 24)]}

    # (25, 41)
    ms[(25, 41)].name = "EAST GATES"
    ms[(25, 41)].description = "Eastern city-state entrance: Towering gates adorned with intricate carvings," \
                               " guarded by vigilant sentinels, mark the grand entry to a thriving metropolis" \
                               " blending history and modernity."

    # (26, 29)
    ms[(26, 29)].description = "Blocked valley passage, boulders from a recent landslide obstruct the way, as " \
                               "a diligent worker clears debris, striving to reopen this vital route amidst " \
                               "the rugged beauty of the scenic landscape."
    ms[(26, 29)].name = "VALLEY"

    # (27, 29)
    ms[(27, 29)].req = ["rocks"]

    # (31, 24)
    ms[(31, 24)].description = "Rugged terrain, sinister caves, and sneaky goblin tribes dominate these " \
                               "perilous elevated lands."
    ms[(31, 24)].entries = {"cave_entrance": ENTRIES["sub_cave_4_0"]}

    # (34, 25)
    ms[(34, 25)].description = "Abandoned woodland hut, dilapidated and forgotten, this rustic abode near the" \
                               " forest stands as a silent witness to nature's reclamation."
    ms[(34, 25)].name = "FOREST"
    ms[(34, 25)].entries = {"hut": ENTRIES["hut_34_25"]}
    ms[(34, 25)].entries["hut"].leave_entry = ms[(34, 25)]

    # (34, 42)
    first_floor = ENTRIES["tower_of_eldra_floor_1"]
    first_floor.leave_entry = ms[(34, 42)]

    second_floor = ENTRIES["tower_of_eldra_floor_2"]
    second_floor.leave_entry = first_floor

    ms[(34, 42)].description = ("Vast, rocky expanse crowned with a solitary wooden tower. The structure "
                                "stands tall, offering sweeping views of the sky and distant horizons.")
    ms[(34, 42)].name = "PLATEAU"
    ms[(34, 42)].entries = {"tower_of_eldra": first_floor}
    ms[(34, 42)].entries["tower_of_eldra"].entries = {"tower_of_eldra_second_floor": second_floor}

    # (36, 42)
    ms[(36, 42)].entries = {"cave": ENTRIES["cave_39_43"]}

    # (34, 51)
    ms[(34, 51)].description = ("Sandy shores meet grassy dunes, where a weathered hut stands, surrounded"
                                " by scattered driftwood and the soothing sound of crashing waves.")
    ms[(34, 51)].name = "COAST"
    ms[(34, 51)].entries = {"coast_hut": ENTRIES["hut_34_51"]}
    ms[(34, 51)].entries["coast_hut"].leave_entry = ms[(34, 51)]

    # (38, 39)
    ms[(38, 39)].description = "Aquiri's portside entrance: Bustling harbor welcomes ships with salty " \
                               "breezes. Weathered docks and colorful boats set the scene for a lively " \
                               "maritime haven in this coastal village."
    ms[(38, 39)].name = "AQUIRI'S PORTSIDE ENTRANCE"

    # (39, 38)
    ms[(39, 38)].description = "Seaside fishing hamlet, colorful boats bob gently in the harbor, while " \
                               "weathered cottages line the shore of this picturesque coastal community. A " \
                               "lone fisherman casts his net into the glistening waters, capturing the " \
                               "essence of maritime tranquility."
    ms[(39, 38)].name = "AQUIRI'S VILLAGE"
    ms[(39, 38)].entries = {"marlins_hut": ENTRIES["house_aquiri_marlin"],
                            "house": ENTRIES["house_aquiri_normal"]}
    ms[(39, 38)].entries["marlins_hut"].leave_entry = ms[(39, 38)]
    ms[(39, 38)].entries["house"].leave_entry = ms[(39, 38)]

    # (39, 39)
    ms[(39, 39)].description = "Seaside fishing hamlet, colorful boats bob gently in the harbor, while " \
                               "weathered cottages line the shore of this picturesque coastal community."
    ms[(39, 39)].entries = {
        "inn": ENTRIES["lyssias_inn"],
        "coast_stone_house": ENTRIES["house_aquiri_stone"],
        "thornes_ship": ENTRIES["thornes_ship"]}

    ms[(39, 39)].entries["inn"].leave_entry = ms[(39, 39)]
    ms[(39, 39)].entries["coast_stone_house"].leave_entry = ms[(39, 39)]
    ms[(39, 39)].entries["thornes_ship"].leave_entry = ms[(39, 39)]

    ms[(39, 39)].entries["inn"].entries = {
        "first_room": ENTRIES["lyssias_first_room"],
        "second_room": ENTRIES["lyssias_second_room"],
        "third_room": ENTRIES["lyssias_third_room"]}
    ms[(39, 39)].entries["inn"].entries["first_room"].leave_entry = ms[(39, 39)].entries["inn"]
    ms[(39, 39)].entries["inn"].entries["second_room"].leave_entry = ms[(39, 39)].entries["inn"]
    ms[(39, 39)].entries["inn"].entries["third_room"].leave_entry = ms[(39, 39)].entries["inn"]
    ms[(39, 39)].name = "AQUIRI'S VILLAGE"

    # (39, 43)
    ms[(39, 43)].entries = {
        "cave": ENTRIES["cave_39_43"]}
    ms[(39, 43)].entries["cave"].leave_entry = ms[(39, 43)]

    ms[(39, 43)].entries["cave"].entries = {
        "coast": ms[(39, 43)],
        "plateu": ms[(35, 42)]}
