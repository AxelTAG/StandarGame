# Imports.
# Local imports.
from biome import Biome
from npc import Npc

# Command line settings.
WIDTH = 92
HEIGHT = 32

# Patron.
PATRON = [" / /\  ", "/ /\ \ ","\ \/ / ", " \/ /  ", " / /\  ", "/ /\ \ ", "\ \/ / ", " \/ /  "]

# Directions.
DIRECTIONS = {0: "1 - NORTH",  1: "2 - EAST", 2: "3 - SOUTH", 3: "4 - WEST"}

# Colors.
WHITE = (255, 255, 255, 255)
PINK = (255, 105, 180, 255)

# Day parts.
DAY_PARTS = ("MORNING", "AFTERNOON", "EVENING", "NIGHT")

# Bioms of map.
BIOMES = {
    "canyon": Biome(
        color=(54, 54, 54, 255),
        description="Shadowy canyon inhabited by fearsome creatures, dark depths, echoing roars, and lurking horrors",
        fight=True,
        mobs=["basilisk", "giant blind spider", "orc", "spectrum"],
        mobs_chances=[30, 50, 10, 30],
        name="CANYON",
        req=["torch"],
        status=[0]),
    "cave": Biome(
        color=(1, 1, 1, 255),
        description="...",
        fight=True,
        mobs=["goblin", "orcs"],
        mobs_chances=[80, 50],
        name="CAVE",
        req=["torch"],
        status=[0]),
    "coast": Biome(
        color=(239, 228, 176, 255),
        description="Seaside with swaying palm trees, echoing waves, and vibrant life.",
        fight=True,
        mobs=["litle slime", "slime"],
        mobs_chances=[5, 30],
        name="COAST",
        req=[],
        status=[0, 1]),
    "dark forest": Biome(
        color=(22, 118, 51, 255),
        description="Shadowy forest of peril, twisted trees loom overhead, their gnarled branches casting eerie "
                    "shadows. ",
        fight=True,
        mobs=["spectral foxshade", "giant spider"],
        mobs_chances=[1, 30],
        name="DARK FOREST",
        req=[],
        status=[0]),
    "death valley": Biome(
        color=(148, 148, 148, 255),
        description="Dreadful dead valley, a chilling abyss where every step deepens the terror within. The air grows "
                    "heavy, and eerie whispers intensify, inducing an unsettling unease as you delve further.",
        fight=True,
        mobs=[""],
        mobs_chances=[0],
        name="DEATH VALLEY",
        req=[],
        status=[0]),
    "fields": Biome(
        color=(115, 231, 29, 255),
        description="Verdant fields, rolling emerald expanses dotted with wildflowers, where gentle breezes carry the "
                    "sweet scent of blooming herbs and distant melodies from hidden creatures in the tall grass.",
        fight=True,
        mobs=["dryad", "slime"],
        mobs_chances=[15, 30],
        name="FIELDS",
        req=[],
        status=[0]),
    "forest": Biome(
        color=(34, 177, 76, 255),
        description="Thick trees, vibrant flora, wildlife, hidden trails, and lurking danger in this treacherous "
                    "forest realm.",
        fight=True,
        mobs=["bandit", "spectral foxshade"],
        mobs_chances=[20, 1],
        name="FOREST",
        req=[],
        status=[0]),
    "frostvale": Biome(
        color=(120, 186, 252, 255),
        description="A pristine, snow-covered expanse where frost-kissed silence reigns. Glistening ice formations "
                    "adorn the landscape, creating an ethereal and serene winter tableau in nature's icy embrace.",
        fight=False,
        mobs=[""],
        mobs_chances=[0],
        name="FROSTVALE",
        req=[],
        status=[0]),
    "gates": Biome(
        color=(200, 191, 231, 255),
        description="Nothing important.",
        fight=False,
        mobs=[""],
        mobs_chances=[0],
        name="GATES",
        req=[],
        status=[0]),
    "highlands": Biome(
        color=(195, 195, 195, 255),
        description="Rugged terrain, sinister caves, and sneaky goblin tribes dominate these perilous elevated lands.",
        fight=True,
        mobs=["goblin"],
        mobs_chances=[40],
        name="HIGHLANDS",
        req=[],
        status=[0]),
    "hills": Biome(
        color=(78, 185, 32, 255),
        description="Undulating landscapes concealing lurking dangers. Treacherous creatures, hidden in the shadows, "
                    "make these hills a realm of risk for those who dare to traverse their slopes.",
        fight=True,
        mobs=["climbing goblin", "troll", "goblin war chief"],
        mobs_chances=[30, 30, 5],
        name="HILLS",
        req=[],
        status=[0]),
    "hut": Biome(
        color=(185, 122, 87, 255),
        description="Nothing important.",
        entries={"hut": Biome(description="Island hut, a cozy retreat adorned with a bed, a table, two "
                                          "chairs, and a window, invites serenity amid nature's whispers.",
                              items=["bed"])},
        fight=False,
        items=[],
        mobs=[""],
        mobs_chances=[0],
        name="HUT",
        req=[],
        status=[0]),
    "island": Biome(
        color=(201, 237, 92, 255),
        description="Island rainforest, dense foliage, vibrant biodiversity, and cascading waterfalls characterize "
                    "this tropical haven of life and greenery.",
        fight=True,
        mobs=["litle slime"],
        mobs_chances=[30],
        name="ISLAND",
        req=[],
        status=[0]),
    "mountains": Biome(
        color=(127, 127, 127, 255),
        description="Nothing important.",
        fight=False,
        mobs=[""],
        mobs_chances=[0],
        name="MOUNTAINS",
        req=["climbing tools"],
        status=[0]),
    "plains": Biome(
        color=(181, 230, 29, 255),
        description="Gentle terrain, waving grasslands, and minimal elevation define this vast, open expanse of natural"
                    " simplicity and beauty.",
        fight=True,
        mobs=["giant slime", "goblin", "slime"],
        mobs_chances=[20, 30, 30],
        name="PLAINS",
        req=[],
        status=[0]),
    "plateau": Biome(
        color=(181, 230, 29, 255),
        description="Elevated plateau, expansive views, flat summits, and resilient flora characterize this "
                    "high-altitude, majestic landscape.",
        fight=True,
        mobs=["slime"],
        mobs_chances=[30],
        name="PLATEAU",
        req=[],
        status=[0]),
    "red": Biome(
        color=(255, 0, 0, 255),
        description="Nothing important.",
        fight=True,
        mobs=[""],
        mobs_chances=[0],
        name="RED",
        req=[],
        status=[0]),
    "river": Biome(
        color=(0, 162, 232, 255),
        description="Nothing important.",
        fight=True,
        mobs=["boat"],
        mobs_chances=[0],
        name="RIVER",
        req=[],
        status=[1]),
    "rocks": Biome(
        color=(85, 80, 85, 255),
        description="Nothing important.",
        fight=False,
        mobs=[""],
        mobs_chances=[0],
        name="ROCKS",
        req=["wings"],
        status=[0]),
    "sea": Biome(
        color=(63, 72, 204, 255),
        description="Nothing important.",
        fight=False,
        mobs=[""],
        mobs_chances=[0],
        name="SEA",
        req=[],
        status=[1]),
    "snow": Biome(
        color=(250, 250, 250, 255),
        description="Nothing important.",
        fight=True,
        mobs=[],
        mobs_chances=[0],
        name="SNOW",
        req=["snow clothing"],
        status=[0]),
    "town": Biome(
        color=(170, 105, 70, 255),
        description="Nothing important.",
        fight=False,
        mobs=[""],
        mobs_chances=[0],
        name="TOWN",
        req=[],
        status=[0]),
    "valley": Biome(
        color=(167, 167, 167, 255),
        description="Desolate, silent valley, cracked earth stretches between imposing cliffs, where an eerie stillness"
                    " envelops the barren landscape, untouched by the whispers of wind or the rustle of life.",
        fight=False,
        mobs=[""],
        mobs_chances=[0],
        name="VALLEY",
        req=[],
        status=[0]),
    "water": Biome(
        color=(128, 255, 255, 255),
        description="Quiet water.",
        fight=False,
        mobs=[""],
        mobs_chances=[0],
        name="WATER",
        req=[],
        status=[1])
    }


ITEMS_EQUIP = {
    "axe": {
        "atk": 4,
        "def": 0,
        "pre": 0,
        "eva": 0,
        "body": "right_hand"},
    "chainmail_armor": {
        "atk": 0,
        "def": 3,
        "pre": 0,
        "eva": 0,
        "body": "chest"},
    "hardened_leather_armor": {
        "atk": 0,
        "def": 2,
        "pre": 0,
        "eva": 0,
        "body": "chest"},
    "harpoon": {
        "atk": 2,
        "def": 0,
        "pre": 0,
        "eva": 0.1,
        "body": "right_hand"},
    "iron_shield": {
        "atk": 0,
        "def": 3,
        "pre": 0,
        "eva": 0,
        "body": "left_hand"},
    "large_bow": {
        "atk": 2,
        "def": 0,
        "pre": 0.15,
        "eva": 0.30,
        "body": "right_hand"},
    "leather_armor": {
        "atk": 0,
        "def": 1,
        "pre": 0.,
        "eva": 0,
        "body": "chest"},
    "leather_boots": {
        "atk": 0,
        "def": 1,
        "pre": 0.,
        "eva": 0,
        "body": "legs"},
    "longsword": {
        "atk": 4,
        "def": 0,
        "pre": 0.05,
        "eva": 0,
        "body": "right_hand"},
    "mesh_boots": {
        "atk": 0,
        "def": 2,
        "pre": 0.,
        "eva": 0,
        "body": "legs"},
    "plate_armor": {
        "atk": 0,
        "def": 4,
        "pre": 0.,
        "eva": 0,
        "body": "chest"},
    "short_sword": {
        "atk": 1,
        "def": 0,
        "pre": 0,
        "eva": 0,
        "body": "right_hand"},
    "spear": {
        "atk": 3,
        "def": 0,
        "pre": 0.05,
        "eva": 0.15,
        "body": "right_hand"},
    "spike_shield": {
        "atk": 1,
        "def": 3,
        "pre": 0,
        "eva": 0,
        "body": "left_hand"},
    "sword": {
        "atk": 3,
        "def": 0,
        "pre": 0.05,
        "eva": 0,
        "body": "right_hand"},
    "tower_shield": {
        "atk": 0,
        "def": 4,
        "pre": 0,
        "eva": 0,
        "body": "left_hand"},
    "wood_shield": {
        "atk": 0,
        "def": 1,
        "pre": 0,
        "eva": 0,
        "body": "left_hand"},
    "None": {
        "atk": 0,
        "def": 0,
        "pre": 0,
        "eva": 0,
        "body": "None"}
}


ITEMS_SELL = {"antidote": 3,
              "axe": 150,
              "basilisk_fangs": 15,
              "bier": 1,
              "bludgeon": 40,
              "bread": 1,
              "chainmail_armor": 150,
              "cheese": 2,
              "fishing_pole": 25,
              "giant_red_potion": 10,
              "giant_silk": 30,
              "hardened_leather_armor": 60,
              "harpoon": 40,
              "iron_shield": 75,
              "large_bow": 110,
              "leather_armor": 35,
              "leather_boots": 25,
              "litle_red_potion": 2,
              "longsword": 175,
              "mesh_boots": 50,
              "plate_armor": 200,
              "red_potion": 5,
              "short_sword": 50,
              "slime_balls": 1,
              "soap": 1,
              "spear": 125,
              "spike_shield": 150,
              "sword": 150,
              "telescope": 125,
              "torch": 10,
              "tower_shield": 150,
              "water": 1,
              "wood_shield": 20,
              "quit": 0}


# MOBS.
MOBS = {
    "bandit": {
        "name": "Bandit",
        "hp": 30,
        "hpmax": 30,
        "atk": 3,
        "def": 2,
        "eva": 0.4,
        "pre": 0.8,
        "c_coef": 1.5,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 40,
        "items": {"gold": 15, "red_potion": 1, "none": None},
        "dc_items": [0.5, 0.7, 1],
        "exp": 4,
    },
    "basilisk": {
        "name": "Basilisk",
        "hp": 80,
        "hpmax": 80,
        "atk": 12,
        "def": 8,
        "eva": 0.6,
        "pre": 0.7,
        "c_coef": 1.7,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 20,
        "items": {"basilisk_fangs": 2, "none": None},
        "dc_items": [0.7, 1],
        "exp": 10
    },
    "climbing goblin": {
        "name": "Climbing Goblin",
        "hp": 35,
        "hpmax": 35,
        "atk": 7,
        "def": 4,
        "eva": 0.3,
        "pre": 0.8,
        "c_coef": 1.5,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 40,
        "items": {"gold": 20, "red_potion": 1, "wood_shield": 1, "none": None},
        "dc_items": [0.5, 0.6, 0.65, 1],
        "exp": 6
    },
    "dragon": {
        "name": "Dragon FrostFire",
        "hp": 10,
        "hpmax": 10,
        "atk": 15,
        "def": 10,
        "eva": 0.5,
        "pre": 0.9,
        "c_coef": 1.5,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 0,
        "items": {"scales": 4121996, "none": None},
        "dc_items": [0.9999999999, 1],
        "exp": 250,
    },
    "dryad": {
        "name": "Dryad",
        "hp": 20,
        "hpmax": 20,
        "atk": 7,
        "def": 10,
        "eva": 0.6,
        "pre": 0.9,
        "c_coef": 1.7,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 50,
        "items": {"none": None},
        "dc_items": [1],
        "exp": 6,
    },
    "giant blind spider": {
        "name": "Giant Blind Spider",
        "hp": 70,
        "hpmax": 70,
        "atk": 10,
        "def": 5,
        "eva": 0.6,
        "pre": 0.8,
        "c_coef": 1.5,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 5,
        "items": {"giant_silk": 1, "none": None},
        "dc_items": [0.5, 1],
        "exp": 10
    },
    "giant slime": {
        "name": "Giant Slime",
        "hp": 40,
        "hpmax": 40,
        "atk": 3,
        "def": 0,
        "eva": 0,
        "pre": 0.65,
        "c_coef": 1.5,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 50,
        "items": {"slime_balls": 2, "red_potion": 1, "none": None},
        "dc_items": [0.5, 0.7, 1],
        "exp": 3
    },
    "giant spider": {
        "name": "Giant Spider",
        "hp": 70,
        "hpmax": 70,
        "atk": 10,
        "def": 5,
        "eva": 0.3,
        "pre": 0.65,
        "c_coef": 1.6,
        "c_chance": 15,
        "poison": 0,
        "c_poison": 0,
        "esc": 30,
        "items": {"giant_silk": 1, "red_potion": 1, "none": None},
        "dc_items": [0.6, 0.8, 1],
        "exp": 8
    },
    "goblin": {
        "name": "Goblin",
        "hp": 15,
        "hpmax": 15,
        "atk": 3,
        "def": 1,
        "eva": 0.3,
        "pre": 0.7,
        "c_coef": 1.5,
        "c_chance": 30,
        "poison": 0,
        "c_poison": 0,
        "esc": 45,
        "items": {"gold": 5, "red_potion": 1, "none": None},
        "dc_items": [0.5, 0.55, 1],
        "exp": 3
    },
    "goblin war chief": {
        "name": "Goblin War Chief",
        "hp": 60,
        "hpmax": 60,
        "atk": 7,
        "def": 4,
        "eva": 0.5,
        "pre": 0.7,
        "c_coef": 1.5,
        "c_chance": 30,
        "poison": 0,
        "c_poison": 0,
        "esc": 35,
        "items": {"gold": 30, "red_potion": 1, "iron_shield": 1, "axe": 1, "none": None},
        "dc_items": [0.8, 0.85, 0.90, 0.95, 1],
        "exp": 8
    },
    "litle slime": {
        "name": "Litle Slime",
        "hp": 10,
        "hpmax": 10,
        "atk": 2,
        "def": 0,
        "eva": 0,
        "pre": 0.8,
        "c_coef": 1.5,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 60,
        "items": {"slime_balls": 1, "litle_red_potion": 1, "none": None},
        "dc_items": [0.3, 0.45, 1],
        "exp": 1
    },
    "orc": {
        "name": "Orc",
        "hp": 35,
        "hpmax": 35,
        "atk": 6,
        "def": 5,
        "eva": 0.3,
        "pre": 0.7,
        "c_coef": 1.5,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 0,
        "items": {"gold": 20, "red_potion": 1, "none": None},
        "dc_items": [0.5, 0.7, 1],
        "exp": 5,
    },
    "poisonous slime": {
        "name": "Poisonous Slime",
        "hp": 20,
        "hpmax": 20,
        "atk": 3,
        "def": 1,
        "eva": 0,
        "pre": 0.7,
        "c_coef": 1.5,
        "c_chance": 20,
        "poison": 1,
        "c_poison": 0.5,
        "esc": 50,
        "items": {"red_potion": 1, "slime_balls": 2, "none": None},
        "dc_items": [0.25, 0.45, 1],
        "exp": 2
    },
    "slime": {
        "name": "Slime",
        "hp": 20,
        "hpmax": 20,
        "atk": 3,
        "def": 1,
        "eva": 0,
        "pre": 0.7,
        "c_coef": 1.5,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 50,
        "items": {"red_potion": 1, "slime_balls": 2, "none": None},
        "dc_items": [0.25, 0.45, 1],
        "exp": 2
    },
    "spectral foxshade": {
        "name": "Spectral Foxshade",
        "hp": 1,
        "hpmax": 1,
        "atk": 10,
        "def": 0,
        "eva": 0,
        "pre": 1,
        "c_coef": 1.7,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 100,
        "items": {"gold": 50, "none": None},
        "dc_items": [0.9, 1],
        "exp": 15
    },
    "spectrum": {
        "name": "Spectrum",
        "hp": 40,
        "hpmax": 40,
        "atk": 10,
        "def": 0,
        "eva": 0.8,
        "pre": 0.8,
        "c_coef": 1.7,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 20,
        "items": {"none": None},
        "dc_items": [1],
        "exp": 12
    },
    "troll": {
        "name": "Troll",
        "hp": 50,
        "hpmax": 50,
        "atk": 7,
        "def": 4,
        "eva": 0.2,
        "pre": 0.75,
        "c_coef": 1.6,
        "c_chance": 20,
        "poison": 0,
        "c_poison": 0,
        "esc": 50,
        "items": {"gold": 15, "red_potion": 1, "bludgeon": 1, "none": None},
        "dc_items": [0.5, 0.6, 0.65, 1],
        "exp": 6
    }
}

# NPCs types.
NPC_TYPES = ["captain", "dragon", "fisherman", "guard", "innkeeper", "lord", "mayor", "merchant", "monk", "traveler",
             "worker"]

# NPCs.
NPC = {
    "whispers": Npc(name="whispers",
                    npc_type="dragon",
                    messages={0: ["Elina...", "Elina...", "...your destiny awaits.", "Follow the whispers of the wind,"
                                  " and come to me.", "Secrets untold and challenges unknown lie ahead.",
                                  "Trust in the unseen path...", "... come to me."]}),

    "captain thorne": Npc(name="captain thorne",
                          npc_type="captain",
                          messages={
                              0: ["Ahoy, traveler. I'm Captain Thorne.",
                                  "You see my ship there? We won't be setting sail today. A dragon's presence spells "
                                  "danger on the open seas. Until the skies are clear, we remain anchored. Better "
                                  "to be safe in port than to risk the wrath of such a fearsome creature.",
                                  "But fear not, when the danger has passed, I'll gladly offer you passage to the "
                                  "next port."]}),

    "captain zelian": Npc(name="captain zelian",
                          npc_type="captain",
                          messages={
                              0: ["Ah, the sea, a fickle friend and fierce foe.",
                                  "Many a ship I've sailed, battling monsters and discovering uncharted isles. "
                                  "The ocean whispers secrets to those who listen.",
                                  "One day, perhaps, the tides will reveal its mysteries to a brave soul like "
                                  "yourself, adventurer."]}),

    "dragon firefrost": Npc(name="dragon firefrost",
                            npc_type="dragon",
                            messages={
                                0: ["Elina...",
                                    "You finally come to me...",
                                    "Destiny calls for a dance of fire and frost between us...",
                                    "Ready your blade..."]}),

    "fisherman marlin": Npc(name="fisherman marlin",
                            npc_type="fisherman",
                            messages={
                                0: ["Ho there, stranger! Fancy a tale from the sea? Ah, the ocean's my life.",
                                    "You know, my brother's a guard in the city, watches over the folks there. "
                                    "Dangerous duty, but he's got a heart as sturdy as a ship's hull.",
                                    "If you ever find yourself in Antina City, look for Guard Lorian. Tell him Marlin "
                                    "from Aqiri says hello."]}),

    "guard lorian": Npc(name="guard lorian",
                        npc_type="guard",
                        messages={
                            0: ["Halt, traveler! Antina City permits only those with proper credentials to pass "
                                "these gates.",
                                "State your business and present your identification, or you shall not venture beyond.",
                                "The safety of our citizens is paramount, and we cannot afford to be lax in these "
                                "trying times."]}),

    "innkeeper mirabelle": Npc(name="innkeeper mirabelle",
                               npc_type="innkeeper",
                               messages={
                                   0: ["Step into Mirabelle's Inn, weary wanderer. Here, amidst the tranquility of "
                                       "Epiiat, find shelter from the trials of the road. With hearty meals and "
                                       "soft beds, let your worries melt away."],
                                   1: ["Interested in accommodations? Take your pick of rooms tailored to your needs."],
                                   2: ["Are you looking to purchase some nourishment? What do you want?"]},
                               answers={
                                   1: "I need to sleep",
                                   2: "Buy food"},
                               buy_items={"bread": 2, "cheese": 4, "soap": 2, "water": 1, "bier": 2, "quit": 0},
                               buy_beds={"main_room": (5, "main_room_key"), "small_room": (3, "small_room_key"),
                                         "quit": (0, "quit")}),

    "lord aric": Npc(name="lord aric",
                     npc_type="lord",
                     messages={
                         0: ["Greetings, traveler. Alas, these are troubled times for our fair city.",
                             "Just days past, a dragon's shadow darkened our skies. Fear lingers in the hearts of our "
                             "citizens. The safety of Antina is at stake, and our once-stalwart walls now seem "
                             "fragile.",
                             "May the goddesses watch over us and protect us."]}),

    "mayor thorian": Npc(name="mayor thorian",
                         npc_type="mayor",
                         messages={
                             0: ["Greetings, traveler, to our humble abode! Epiiat is open to all seeking refuge.",
                                 "However, I must caution you—recently, the once-tranquil caves to the north have "
                                 "become infested with Goblins and other nefarious beings.",
                                 "We fear a sinister leader guides them.",
                                 "Be vigilant on your journey through our beloved town and beyond, and may the "
                                 "Goddesses guide your steps."]}),

    "merchant bryson": Npc(name="merchant bryson",
                           npc_type="merchant",
                           messages={
                               0: ["Ah, welcome, welcome! Peruse my wares, brave one. From enchanted potions to sturdy"
                                   " shields",
                                   "Bryson's Emporium has all you need for your journey.",
                                   "Each item tells a tale, and every purchase brings you one step closer to becoming "
                                   "a legend. Don't hesitate to ask if you seek something specific, for in this square,"
                                   " dreams and adventures await!"],
                               1: ["What do you want to buy?"],
                               2: ["What do you want to sell?"]},
                           answers={
                               1: "Buy",
                               2: "Sell"},
                           buy_items={"leather_armor": 75, "leather_boots": 60, "litle_red_potion": 5,
                                      "red_potion": 10, "short_sword": 100, "wood_shield": 50, "torch": 20,
                                      "quit": 0}),

    "merchant elden": Npc(name="merchant elden",
                          npc_type="merchant",
                          messages={0: ["Hail, warrior! Seek the finest blades and armor in Antina? Forge Master Elden "
                                        "crafts each piece with skill and care. From gleaming swords to resilient "
                                        "shields, my forge yields the tools to shape your destiny.",
                                        "Arm yourself, adventurer, and may the battles you face be victorious!"],
                                    1: ["What do you want to buy?"],
                                    2: ["What do you want to sell?"]},
                          answers={
                              1: "Buy",
                              2: "Sell"},
                          buy_items={"axe": 280, "chainmail_armor": 300, "large_bow": 220, "longsword": 350,
                                     "iron_shield": 130, "mesh_boots": 100, "plate_armor": 400, "spear": 250,
                                     "spike_shield": 150, "tower_shield": 150, "quit": 0}),

    "merchant roland": Npc(name="merchant roland",
                           npc_type="merchant",
                           messages={0: ["Greetings, noble traveler! Step into Roland's Emporium, where treasures and "
                                         "trinkets await your discerning eye. From potions to weapons, my wares are "
                                         "the finest in Antina.",
                                         "Peruse at your leisure, and may your coffers overflow with the spoils of a "
                                         "grand adventure!"],
                                     1: ["What do you want to buy?"],
                                     2: ["What do you want to sell?"]},
                           answers={
                               1: "Buy",
                               2: "Sell"},
                           buy_items={"giant_red_potion": 15, "red_potion": 10, "sword": 300, "iron_shield": 150,
                                      "torch": 20, "quit": 0}),

    "merchant selena": Npc(name="merchant selena",
                           npc_type="merchant",
                           messages={
                               0: ["Ahoy, brave one! Step right up and behold the treasures of Aqiri's Market!",
                                   "From the finest catches of the sea to enchanted trinkets, Selena's Wares has all "
                                   "you desire. A purchase to aid your journey, perhaps?",
                                   "Sail through our goods, and may your pouch grow lighter with satisfaction!"],
                               1: ["What do you want to buy?"],
                               2: ["What do you want to sell?"]},
                           answers={
                               1: "Buy",
                               2: "Sell"},
                           buy_items={"harpoon": 150, "hardened_leather_armor": 120, "red_potion": 10,
                                      "fishing_pole": 9999, "wood_shield": 50, "telescope": 200, "quit": 0}),

    "traveler elara": Npc(
        name="traveler elara",
        npc_type="traveler",
        messages={
            0: ["Greetings, seeker of paths! If you yearn to traverse the mighty mountain range that veils our"
                " land, head eastward.", "Beyond the emerald canopy and whispering trees lies a hidden valley. It "
                "weaves through the ancient peaks, offering passage to those who dare to journey.", "Take heed, for "
                "the woods conceal both mystery and peril, but the call of adventure echoes through the leaves. May "
                "the spirits guide your way, brave traveler."],
            1: ["Northward, the land ascends into highlands infested with goblins and other vile creatures. A "
                "challenge for even the most seasoned adventurer."],
            2: ["To the south, dense woodlands stretch as far as the eye can see.", "An enchanting realm, but one "
                "must tread cautiously, for shadows dance amidst the trees."],
            3: ["Nay, brave one. The west remains a mystery to me. My journey has yet to unveil the secrets concealed "
                "in those unexplored lands.", "Perhaps one day, the winds of fate will carry me in that direction."]},
        leave_message=["May the spirits guide your way, brave traveler."],
        answers={
            1: "What lies to the north?",
            2: "And what of the southern lands?",
            3: "What about the western reaches? Have you ventured there?"}),

    "traveler elinor": Npc(name="traveler elinor",
                           npc_type="traveler",
                           messages={
                               0: ["Alas, the city gates remain closed to me. But fear not, fellow wanderer!",
                                   "To the east lies the charming fishing village of Aquiri. A quaint haven where the"
                                   " sea breeze dances with the scent of salt and adventure.",
                                   "Seek refuge there, share tales with the fishermen, and who knows, perhaps your "
                                   "path will intertwine with the whims of destiny. May the winds guide your steps, "
                                   "for there is always another path to tread."]}),

    "traveler kaelin": Npc(name="traveler kaelin",
                           npc_type="traveler",
                           messages={
                               0: ["Hail, fellow wanderer. I've treaded the southern realms, through the treacherous "
                                   "Dark Forest.",
                                   "A word of caution, brave soul – the woods conceal more than beauty. Dark whispers "
                                   "and lurking dangers await. I'd advise against venturing there unless your courage "
                                   "knows no bounds.",
                                   "May your travels be safer than mine, and the path you choose be bathed in the "
                                   "light of wisdom."]}),

    "traveler seraph": Npc(name="traveler seraph",
                           npc_type="traveler",
                           messages={0: ["Ah, greetings, fellow wayfarer! Stuck, just like me, eh? Gorrick here "
                                         "mentioned some caves to the north that might lead us across.", "Aye, those "
                                         "caves are an option, but beware! Lately, they've become a haven for Goblins "
                                         "and other foul creatures.", "A perilous journey awaits, my friend. Tread "
                                         "carefully if you choose that path."]}),

    "traveler sylas": Npc(name="traveler sylas",
                          npc_type="traveler",
                          messages={
                              0: ["Greetings, wanderer. A word of wisdom for your journey: always embrace exploration.",
                                  "Hidden wonders and untold tales await those who venture beyond the familiar. May "
                                  "your steps be guided by curiosity, and may the world unveil its mysteries before "
                                  "you."]}),

    "traveler thaldir": Npc(name="traveler thaldir",
                            npc_type="traveler",
                            messages={
                                0: ["Greetings, seeker of fortune. Remember, in every step, 'tis wise to look around "
                                    "and check. Secrets often hide where the eye does not linger.",
                                    "May the journey unveil the unseen, brave one."]}),

    "worker gorrick": Npc(name="worker gorrick",
                          npc_type="worker",
                          messages={
                              0: ["Hail, traveler! The path ahead is blocked, and only through my efforts can it be "
                                  "opened. Alas, it'll take time."]}),
}
