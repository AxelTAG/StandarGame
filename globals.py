# Command line settings.
WIDTH = 92
HEIGHT = 32

# Patron.
PATRON = [" / /\  ", "/ /\ \ ","\ \/ / ", " \/ /  ", " / /\  ", "/ /\ \ ", "\ \/ / ", " \/ /  "]

# Colors.
WHITE = (255, 255, 255, 255)

# Day parts.
DAY_PARTS = ("MORNING", "AFTERNOON", "EVENING", "NIGHT")

# Bioms of map.
BIOMS = {
    "canyon": {
        "t": "CANYON",
        "e": True,
        "e_list": ["basilisk", "giant blind spider", "orcs", "spectrum"],
        "e_chance": [30, 50, 10, 30],
        "r": ["torch", "walk"],
        "d": "Shadowy canyon inhabited by fearsome creatures, dark depths, echoing roars, and lurking horrors",
        "c": (54, 54, 54, 255)},
    "cave": {
        "t": "CAVE",
        "e": False,
        "e_list": ["goblin", "orcs"],
        "e_chance": [80, 50],
        "r": ["torch", "walk"],
        "d": "Nothing important.",
        "c": (1, 1, 1, 255)},
    "coast": {
        "t": "COAST",
        "e": True,
        "e_list": ["litle slime", "slime"],
        "e_chance": [5, 30],
        "r": [],
        "d": "Seaside with swaying palm trees, echoing waves, and vibrant life.",
        "c": (239, 228, 176, 255)},
    "dark forest": {
        "t": "DARK FOREST",
        "e": True,
        "e_list": ["spectral foxshade", "giant spider"],
        "e_chance": [1, 30],
        "r": ["walk"],
        "d": "Shadowy forest of peril, twisted trees loom overhead, their gnarled branches casting eerie shadows. "
             "Giant spiders lurk among the dense undergrowth, adding a sinister layer to the foreboding darkness.",
        "c": (22, 118, 51, 255)},
    "death valley": {
        "t": "DEATH VALLEY",
        "e": True,
        "e_list": [""],
        "e_chance": [0],
        "r": ["walk"],
        "d": "Dreadful dead valley, a chilling abyss where every step deepens the terror within. The air grows heavy,"
             " and eerie whispers intensify, inducing an unsettling unease as you delve further.",
        "c": (148, 148, 148, 255)},
    "fields": {
        "t": "FIELDS",
        "e": True,
        "e_list": ["slime"],
        "e_chance": [30],
        "r": ["walk"],
        "d": "Verdant fields, rolling emerald expanses dotted with wildflowers, where gentle breezes carry the sweet "
             "scent of blooming herbs and distant melodies from hidden creatures in the tall grass.",
        "c": (115, 231, 29, 255)},
    "forest": {
        "t": "FOREST",
        "e": True,
        "e_list": ["bandit", "spectral foxshade"],
        "e_chance": [20, 1],
        "r": ["walk"],
        "d": "Thick trees, vibrant flora, wildlife, hidden trails, and lurking danger in this treacherous "
             "forest realm.",
        "c": (34, 177, 76, 255)},
    "frostvale": {
        "t": "FROSTVALE",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "A pristine, snow-covered expanse where frost-kissed silence reigns. Glistening ice formations adorn the "
             "landscape, creating an ethereal and serene winter tableau in nature's icy embrace.",
        "c": (120, 186, 252, 255)},
    "gates": {
        "t": "GATES",
        "e": False,
        "e_list": [""],
        "e_chance": [0],
        "r": ["walk"],
        "d": "Nothing important.",
        "c": (200, 191, 231, 255)},
    "highlands": {
        "t": "HIGHLANDS",
        "e": True,
        "e_list": ["goblin"],
        "e_chance": [40],
        "r": ["walk"],
        "d": "Rugged terrain, sinister caves, and sneaky goblin tribes dominate these perilous elevated lands.",
        "c": (195, 195, 195, 255)},
    "hills": {
        "t": "HILLS",
        "e": True,
        "e_list": ["climbing goblin", "troll", "goblin war chief"],
        "e_chance": [30, 30, 5],
        "r": ["walk"],
        "d": "Undulating landscapes concealing lurking dangers. Treacherous creatures, hidden in the shadows, make "
             "these hills a realm of risk for those who dare to traverse their slopes.",
        "c": (78, 185, 32, 255)},
    "hut": {
        "t": "ELINA'S HUT",
        "e": False,
        "e_list": [""],
        "e_chance": [0],
        "r": ["walk"],
        "d": "Nothing important.",
        "c": (185, 122, 87, 255)},
    "island": {
        "t": "ISLAND",
        "e": True,
        "e_list": ["litle slime"],
        "e_chance": [30],
        "r": ["walk"],
        "d": "Island rainforest, dense foliage, vibrant biodiversity, and cascading waterfalls characterize this"
             " tropical haven of life and greenery.",
        "c": (201, 237, 92, 255)},
    "mountains": {
        "t": "MOUNTAINS",
        "e": False,
        "e_list": [""],
        "e_chance": [0],
        "r": ["climbing tools"],
        "d": "Nothing important.",
        "c": (127, 127, 127, 255)},
    "plains": {
        "t": "PLAINS",
        "e": True,
        "e_list": ["giant slime", "goblin", "slime"],
        "e_chance": [20, 30, 30],
        "r": ["walk"],
        "d": "Gentle terrain, waving grasslands, and minimal elevation define this vast, "
             "open expanse of natural simplicity and beauty.",
        "c": (181, 230, 29, 255)},
    "plateau": {
        "t": "PLATEAU",
        "e": True,
        "e_list": ["slime"],
        "e_chance": [30],
        "r": ["walk"],
        "d": "Elevated plateau, expansive views, flat summits, and resilient flora characterize this high-altitude, "
             "majestic landscape.",
        "c": (181, 230, 29, 255)},
    "red": {
        "t": "RED",
        "e": True,
        "e_list": [""],
        "e_chance": [0],
        "r": [],
        "d": "Nothing important.",
        "c": (255, 0, 0, 255)},
    "river": {
        "t": "RIVER",
        "e": True,
        "e_list": ["boat"],
        "e_chance": [0],
        "r": ["boat"],
        "d": "Nothing important.",
        "c": (0, 162, 232, 255)},
    "rocks": {
        "t": "ROCKS",
        "e": False,
        "e_list": [""],
        "e_chance": [0],
        "r": ["wings"],
        "d": "Nothing important.",
        "c": (85, 80, 85, 255)},
    "sea": {
        "t": "SEA",
        "e": False,
        "e_list": [""],
        "e_chance": [0],
        "r": ["boat"],
        "d": "Nothing important.",
        "c": (63, 72, 204, 255)},
    "snow": {
        "t": "SNOW",
        "e": True,
        "e_list": [],
        "e_chance": [0],
        "r": ["walk", "snow clothing"],
        "d": "Nothing important.",
        "c": (250, 250, 250, 255)},
    "town": {
        "t": "TOWN",
        "e": False,
        "e_list": [""],
        "e_chance": [0],
        "r": ["walk"],
        "d": "Nothing important.",
        "c": (170, 105, 70, 255)},
    "valley": {
        "t": "VALLEY",
        "e": False,
        "e_list": [""],
        "e_chance": [0],
        "r": ["walk"],
        "d": "Desolate, silent valley, cracked earth stretches between imposing cliffs, where an eerie stillness "
             "envelops the barren landscape, untouched by the whispers of wind or the rustle of life.",
        "c": (167, 167, 167, 255)},
    "water": {
        "t": "WATER",
        "e": False,
        "e_list": [""],
        "e_chance": [0],
        "r": ["boat"],
        "d": "Quiet water.",
        "c": (128, 255, 255, 255)}
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


ITEMS_SELL = {"axe": 150,
              "basilisk_fangs": 15,
              "chainmail_armor": 150,
              "litle_red_potion": 2,
              "fishing_pole": 9999,
              "giant_red_potion": 10,
              "giant_silk": 30,
              "hardened_leather_armor": 60,
              "harpoon": 40,
              "iron_shield": 75,
              "large_bow": 110,
              "leather_armor": 35,
              "leather_boots": 25,
              "longsword": 175,
              "mesh_boots": 50,
              "plate_armor": 200,
              "red_potion": 5,
              "short_sword": 50,
              "slime_balls": 1,
              "spear": 125,
              "spike_shield": 150,
              "sword": 150,
              "torch": 10,
              "tower_shield": 150,
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
        "items": {"gold": 10, "red_potion": 1, "none": None},
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
        "items": {"basilisk_fangs": 2, "none": None},
        "dc_items": [0.5, 1],
        "exp": 10
    },
    "climbing goblin": {
        "name": "Climbing Goblin",
        "hp": 35,
        "hpmax": 35,
        "atk": 6,
        "def": 4,
        "eva": 0.3,
        "pre": 0.8,
        "items": {"gold": 10, "red_potion": 1, "wood_shield": 1, "none": None},
        "dc_items": [0.5, 0.6, 0.65, 1],
        "exp": 4
    },
    "dragon": {
        "name": "Dragon FrostFire",
        "hp": 10,
        "hpmax": 10,
        "atk": 15,
        "def": 10,
        "eva": 0.5,
        "pre": 0.9,
        "items": {"scales": 4121996, "none": None},
        "dc_items": [0.9999, 1],
        "exp": 0,
    },
    "giant blind spider": {
        "name": "Giant Blind Spider",
        "hp": 70,
        "hpmax": 70,
        "atk": 10,
        "def": 5,
        "eva": 0.6,
        "pre": 0.8,
        "items": {"giant_silk": 1, "red_potion": 1, "none": None},
        "dc_items": [0.5, 0.8, 1],
        "exp": 8
    },
    "giant slime": {
        "name": "Giant Slime",
        "hp": 40,
        "hpmax": 40,
        "atk": 3,
        "def": 0,
        "eva": 0,
        "pre": 0.65,
        "items": {"slime_balls": 2, "red_potion": 1, "none": None},
        "dc_items": [0.5, 0.7, 1],
        "exp": 2
    },
    "giant spider": {
        "name": "Giant Spider",
        "hp": 70,
        "hpmax": 70,
        "atk": 10,
        "def": 5,
        "eva": 0.3,
        "pre": 0.65,
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
        "items": {"gold": 5, "red_potion": 1, "none": None},
        "dc_items": [0.5, 0.55, 1],
        "exp": 3
    },
    "goblin war chief": {
        "name": "Goblin War Chief",
        "hp": 60,
        "hpmax": 60,
        "atk": 7,
        "def": 2,
        "eva": 0.5,
        "pre": 0.7,
        "items": {"gold": 15, "red_potion": 1, "iron_shield": 1, "axe": 1, "none": None},
        "dc_items": [0.8, 0.90, 0.95, 0.98, 1],
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
        "items": {"slime_balls": 1, "none": None},
        "dc_items": [0.3, 1],
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
        "items": {"gold": 15, "red_potion": 1, "none": None},
        "dc_items": [0.5, 0.7, 1],
        "exp": 5,
    },
    "slime": {
        "name": "Slime",
        "hp": 20,
        "hpmax": 20,
        "atk": 3,
        "def": 1,
        "eva": 0,
        "pre": 0.7,
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
        "items": {"none": None},
        "dc_items": [1],
        "exp": 10
    },
    "troll": {
        "name": "Troll",
        "hp": 50,
        "hpmax": 50,
        "atk": 6,
        "def": 2,
        "eva": 0.2,
        "pre": 0.75,
        "items": {"gold": 15, "red_potion": 1, "bludgeon": 1, "none": None},
        "dc_items": [0.5, 0.6, 0.65, 1],
        "exp": 4
    }
}


# MAP SETTING format dic[].
MAP_SETTING = {
    "(0, 0)": {
        "t": "HUT",
        "e": False,
        "e_list": [""],
        "e_chance": [0],
        "r": ["walk"],
        "d": "Island hut, a cozy retreat adorned with a bed, a table, two chairs, and a window, invites serenity amid "
             "nature's whispers.",
        "items": ["bed"],
        "npc": [],
        "entries": [],
        "c": (185, 122, 87, 255)},
    "(1, 23)": {
        "t": "HUT",
        "e": False,
        "e_list": [""],
        "e_chance": [0],
        "r": ["walk"],
        "d": "Isolated shelter amid dangers, where rustling leaves and distant howls suggest that safety within is "
             "uncertain at best.",
        "items": ["bed"],
        "npc": [],
        "entries": [],
        "c": (185, 122, 87, 255)},
    "(2, 1)": {
        "t": "COAST",
        "e": True,
        "e_list": ["slime"],
        "e_chance": [30],
        "r": ["walk"],
        "d": "Seaside with anchored boat, echoing waves and vibrant coastal life.",
        "items": ["boat"],
        "npc": [],
        "entries": [],
        "c": (239, 228, 176, 255)},
    "(6, 2)": {
        "t": "COAST",
        "e": True,
        "e_list": ["slime"],
        "e_chance": [30],
        "r": ["walk"],
        "d": "Seaside with anchored boat, echoing waves and vibrant coastal life. A solitary figure stands at the "
             "water's edge, gazing out into the vastness of the sea, captivated by the rhythmic dance of the waves and "
             "the boundless horizon stretching before them.",
        "items": ["boat"],
        "npc": ["captain zelian"],
        "entries": [],
        "c": (239, 228, 176, 255)},
    "(9, 4)": {
        "t": "NORTHERN GATES",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Northern village entrance, sturdy gates open to a cozy haven, framed by rolling hills and welcoming "
             "cottages.",
        "items": [],
        "npc": ["traveler thaldir"],
        "entries": [],
        "c": (200, 191, 231, 255)},
    "(9, 5)": {
        "t": "TOWN",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Inn district, cozy tavern, lively marketplace, and quaint cottages surround the inviting inn, creating "
             "a charming and bustling neighborhood. A charismatic merchant hawks wares in the heart of this bustling "
             "community hub.",
        "items": ["bed"],
        "npc": ["merchant bryson", "traveler sylas"],
        "entries": ["inn"],
        "c": (170, 105, 70, 255)},
    "(9, 17)": {
        "t": "EASTERN GATES",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Eastern gateway to Antina: Mighty arches frame the welcoming path, guiding travelers through a "
             "bustling thoroughfare toward the heart of the enchanting city.",
        "items": [],
        "npc": ["traveler kaelin"],
        "entries": [],
        "c": (170, 105, 70, 255)},
    "(10, 4)": {
        "t": "TOWN CENTER",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Village hub, Mayor's office, bustling square, and a quaint temple create the heart of community life.",
        "items": [],
        "npc": ["mayor thorian"],
        "entries": [],
        "c": (170, 105, 70, 255)},
    "(10, 5)": {
        "t": "SOUTHERN GATES",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Southern gateway, welcoming gates, cobblestone paths, and a charming, serene atmosphere greet visitors.",
        "items": [],
        "npc": ["traveler elara"],
        "entries": [],
        "c": (200, 191, 231, 255)},
    "(10, 16)": {
        "t": "ANTINA'S CATHEDRAL",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Majestic spires pierce the sky, casting a divine aura over cobblestone squares. The sacred structure "
             "beckons pilgrims and whispers tales of ancient reverence",
        "items": [],
        "npc": [],
        "entries": ["cathedral"],
        "c": (200, 191, 231, 255)},
    "(10, 17)": {
        "t": "ANTINA CITY",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Antina's post-gate district, winding streets lead to residential quarters and training grounds. Stone "
             "structures bear the weight of history, weaving a tapestry of everyday life beyond the bustling entrance "
             "gates.",
        "items": [],
        "npc": [],
        "entries": [],
        "c": (170, 105, 70, 255)},
    "(10, 18)": {
        "t": "ANTINA'S TAVERN DISTRICT",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Cobbled lanes weave among lively taverns and cozy inns, offering weary travelers respite. A symphony of"
             " laughter, music, and clinking tankards fills the air, creating an inviting atmosphere.",
        "items": ["bed"],
        "npc": [],
        "entries": ["inn"],
        "c": (200, 191, 231, 255)},
    "(11, 15)": {
        "t": "ANTINA'S CASTLE",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Antina's castle precinct, towering fortress crowned with turrets dominates the cityscape. Home to "
             "nobility and adorned with banners, the castle overlooks sprawling courtyards, embodying the seat "
             "of power in Antina.",
        "items": [],
        "npc": ["lord aric"],
        "entries": ["castle"],
        "c": (200, 191, 231, 255)},
    "(11, 16)": {
        "t": "ANTINA'S FOUNTAIN SQUARE",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "A grand centerpiece adorned with intricate sculptures, where cascading waters mirror the city's "
             "vibrancy, inviting residents and visitors to linger in its refreshing ambiance.",
        "items": [],
        "npc": [],
        "entries": [],
        "c": (200, 191, 231, 255)},
    "(11, 17)": {
        "t": "ANTINA'S MARKET",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Antina's medieval hub, majestic castle towers overlook bustling market squares, where knights, "
             "merchants, and mystics converge. Cobblestone streets wind through diverse districts, echoing with the "
             "city's vibrant heartbeat.",
        "items": [],
        "npc": ["merchant roland"],
        "entries": [],
        "c": (200, 191, 231, 255)},
    "(11, 18)": {
        "t": "ANTINA'S RESIDENTIAL QUARTER",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Quaint abodes line tranquil streets, adorned with blooming gardens. A serene enclave where the city's "
             "heartbeat echoes in the everyday rhythms of its residents.",
        "items": [],
        "npc": [],
        "entries": [],
        "c": (200, 191, 231, 255)},
    "(11, 24)": {
        "t": "FROSTVALE",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Frozen valley under the watchful gaze of a dragon, crystalized landscapes echo with the dragon's silent"
             " vigil, as icy winds and shimmering frost create an otherworldly ambiance.",
        "items": [],
        "npc": ["dragon firefrost"],
        "entries": [],
        "c": (120, 186, 252, 255)},
    "(12, 16)": {
        "t": "ANTINA'S RESIDENTIAL QUARTER",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Quaint abodes line tranquil streets, adorned with blooming gardens. A serene enclave where the city's "
             "heartbeat echoes in the everyday rhythms of its residents.",
        "items": [],
        "npc": [],
        "entries": [],
        "c": (200, 191, 231, 255)},
    "(12, 17)": {
        "t": "ANTINA CITY",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk", "permission"],
        "d": "Antina's post-gate district, winding streets lead to residential quarters and training grounds. Stone "
             "structures bear the weight of history, weaving a tapestry of everyday life beyond the bustling entrance "
             "gates.",
        "items": [],
        "npc": [],
        "entries": [],
        "c": (170, 105, 70, 255)},
    "(12, 18)": {
        "t": "ANTINA'S ARENA",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Antina's arena district: Colossal stone coliseum stands amidst cheering crowds. Brave warriors clash "
             "within, seeking glory and honor, while merchants peddle wares to the fervent spectators, creating an "
             "electrifying atmosphere.",
        "items": [],
        "npc": ["merchant elden"],
        "entries": [],
        "c": (200, 191, 231, 255)},
    "(13, 0)": {
        "t": "HIGHLANDS",
        "e": True,
        "e_list": ["goblin", "orc"],
        "e_chance": ["40", "90"],
        "r": ["walk"],
        "d": "Rugged terrain, sinister caves, and sneaky goblin tribes dominate these perilous elevated lands.",
        "items": [],
        "npc": [],
        "entries": ["cave"],
        "c": (195, 195, 195, 255)},
    "(13, 17)": {
        "t": "EAST GATES",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Eastern city-state entrance: Towering gates adorned with intricate carvings, guarded by vigilant "
             "sentinels, mark the grand entry to a thriving metropolis blending history and modernity.",
        "items": [],
        "npc": ["guard lorian", "traveler elinor"],
        "entries": [],
        "c": (200, 191, 231, 255)},
    "(14, 5)": {
        "t": "VALLEY",
        "e": True,
        "e_list": ["slime"],
        "e_chance": [30],
        "r": ["walk"],
        "d": "Blocked valley passage, boulders from a recent landslide obstruct the way, as a diligent worker clears "
             "debris, striving to reopen this vital route amidst the rugged beauty of the scenic landscape.",
        "items": [],
        "npc": ["worker gorrick", "traveler seraph"],
        "entries": [],
        "c": (167, 167, 167, 255)},
    "(15, 5)": {
        "t": "ROCKS",
        "e": True,
        "e_list": ["slime"],
        "e_chance": [30],
        "r": ["wings"],
        "d": "Nothing important here.",
        "items": [],
        "npc": [],
        "entries": [],
        "c": (85, 80, 85, 255)},
    "(18, 24)": {
        "t": "HUT",
        "e": False,
        "e_list": [""],
        "e_chance": [0],
        "r": ["walk"],
        "d": "Abandoned woodland hut, dilapidated and forgotten, this rustic abode near the forest stands as a silent "
             "witness to nature's reclamation.",
        "items": ["bed"],
        "npc": [],
        "entries": [],
        "c": (185, 122, 87, 255)},
    "(19, 0)": {
        "t": "HIGHLANDS",
        "e": True,
        "e_list": ["goblin", "orc"],
        "e_chance": ["40", "90"],
        "r": ["walk"],
        "d": "Rugged terrain, sinister caves, and sneaky goblin tribes dominate these perilous elevated lands.",
        "items": [],
        "npc": [],
        "entries": ["cave"],
        "c": (195, 195, 195, 255)},
    "(22, 1)": {
        "t": "HUT",
        "e": False,
        "e_list": [""],
        "e_chance": [0],
        "r": ["walk"],
        "d": "Abandoned woodland hut, dilapidated and forgotten, this rustic abode near the forest stands as a silent "
             "witness to nature's reclamation.",
        "items": ["bed"],
        "npc": [],
        "entries": [],
        "c": (185, 122, 87, 255)},
    "(27, 14)": {
        "t": "VILLAGE",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Seaside fishing hamlet, colorful boats bob gently in the harbor, while weathered cottages line the shore "
             "of this picturesque coastal community. A lone fisherman casts his net into the glistening waters, "
             "capturing the essence of maritime tranquility.",
        "items": [],
        "npc": ["fisherman marlin"],
        "entries": [],
        "c": (170, 105, 70, 255)},
    "(27, 15)": {
        "t": "VILLAGE",
        "e": False,
        "e_list": [],
        "e_chance": [],
        "r": ["walk"],
        "d": "Seaside fishing hamlet, colorful boats bob gently in the harbor, while weathered cottages line the shore "
             "of this picturesque coastal community.",
        "items": ["bed"],
        "npc": ["merchant selena"],
        "entries": [],
        "c": (170, 105, 70, 255)}
}


# NPCs.
NPC = {
    "whispers": [["Elina...", "Elina...", "...your destiny awaits.", "Follow the whispers of the wind, and come to me.",
                  "Secrets untold and challenges unknown lie ahead.", "Trust in the unseen path...", "... come to me."],
                 [], [], [0]],
    "captain zelian": [["Ah, the sea, a fickle friend and fierce foe.", "Many a ship I've sailed, battling monsters "
                        "and discovering uncharted isles. The ocean whispers secrets to those who listen.", "Legend "
                        "speaks of a mystical realm beneath these waves, hidden from mortal eyes.", "One day, perhaps, "
                        "the tides will reveal its mysteries to a brave soul like yourself, adventurer."],
                       [], [], [0]],
    "dragon firefrost": [["Elina...", "You finally come to me...", "Destiny calls for a dance of fire and frost "
                          "between us...", "Ready your blade..."],
                         [], [], [0]],
    "fisherman marlin": [["Ho there, stranger! Fancy a tale from the sea? Ah, the ocean's my life.", "You know, my "
                          "brother's a guard in the city, watches over the folks there. Dangerous duty, but he's got a "
                          "heart as sturdy as a ship's hull.", "If you ever find yourself in Antina City, look for "
                          "Guard Lorian. Tell him Marlin from Aqiri says hello."],
                         [], [], [0]],
    "guard lorian": [["Halt, traveler! Antina City permits only those with proper credentials to pass these gates.",
                      "State your business and present your identification, or you shall not venture beyond.", "The "
                      "safety of our citizens is paramount, and we cannot afford to be lax in these trying times."],
                     [], [], [0, 0, 0]],
    "lord aric": [["Greetings, traveler. Alas, these are troubled times for our fair city.", "Just days past, a "
                   "dragon's shadow darkened our skies. Fear lingers in the hearts of our citizens. The safety of "
                   "Antina is at stake, and our once-stalwart walls now seem fragile.", "May the goddesses watch "
                   "over us and protect us."],
                  [], [], [0, 0, 0]],
    "merchant bryson": [["Ah, welcome, welcome! Peruse my wares, brave one. From enchanted potions to sturdy shields, "
                         "Bryson's Emporium has all you need for your journey.", "Each item tells a tale, and every "
                         "purchase brings you one step closer to becoming a legend. Don't hesitate to ask if you seek "
                         "something specific, for in this square, dreams and adventures await!"],
                        [["buy", ["What do you want to buy?"]], ["sell", ["What do you want to sell?"]]],
                        [{"leather_armor": 75, "leather_boots": 60, "litle_red_potion": 5, "red_potion": 10,
                          "short_sword": 100, "wood_shield": 50, "torch": 20, "quit": 0}], [0, 0, 0]],
    "merchant elden": [["Hail, warrior! Seek the finest blades and armor in Antina? Forge Master Elden crafts each "
                        "piece with skill and care. From gleaming swords to resilient shields, my forge yields the"
                        " tools to shape your destiny. ",
                        "Arm yourself, adventurer, and may the battles you face be victorious!"],
                       [["buy", ["What do you want to buy?"]], ["sell", ["What do you want to sell?"]]],
                       [{"axe": 280, "chainmail_armor": 300, "large_bow": 220, "longsword": 350, "iron_shield": 130, "mesh_boots": 100, "plate_armor": 400,
                         "spear": 250, "spike_shield": 150, "tower_shield": 150, "quit": 0}], [0, 0, 0]],
    "merchant roland": [["Greetings, noble traveler! Step into Roland's Emporium, where treasures and trinkets await "
                         "your discerning eye. From potions to weapons, my wares are the finest in Antina.", "Peruse "
                         "at your leisure, and may your coffers overflow with the spoils of a grand adventure!"],
                        [["buy", ["What do you want to buy?"]], ["sell", ["What do you want to sell?"]]],
                        [{"giant_red_potion": 15, "red_potion": 10, "sword": 300, "iron_shield": 150, "torch": 20, "quit": 0}], [0, 0, 0]],
    "mayor thorian": [["Greetings, traveler, to our humble abode! Epiiat is open to all seeking refuge.", "However, I "
                       "must caution you—recently, the once-tranquil caves to the north have become infested with "
                       "Goblins and other nefarious beings.", "We fear a sinister leader guides them.", "Be vigilant on"
                       " your journey through our beloved town and beyond, and may the Goddesses guide your steps."],
                      [], [], [0]],
    "merchant selena": [["Ahoy, brave one! Step right up and behold the treasures of Aqiri's Market!", "From the "
                         "finest catches of the sea to enchanted trinkets, Selena's Wares has all you desire. A "
                         "purchase to aid your journey, perhaps?", "Sail through our goods, and may your pouch grow "
                         "lighter with satisfaction!"],
                        [["buy", ["What do you want to buy?"]], ["sell", ["What do you want to sell?"]]],
                        [{"harpoon": 150, "hardened_leather_armor": 120, "red_potion": 10, "fishing_pole": 9999,
                          "wood_shield": 50, "quit": 0}], [0, 0, 0]],
    "traveler elara": [["Greetings, seeker of paths! If you yearn to traverse the mighty mountain range that veils our"
                        " land, head eastward.", "Beyond the emerald canopy and whispering trees lies a hidden valley. "
                        "It weaves through the ancient peaks, offering passage to those who dare to journey.", "Take "
                        "heed, for the woods conceal both mystery and peril, but the call of adventure echoes through"
                        " the leaves. May the spirits guide your way, brave traveler."],
                       [["What lies to the north?", ["Northward, the land ascends into highlands infested with "
                         "goblins and other vile creatures. A challenge for even the most seasoned adventurer."]],
                        ["And what of the southern lands?", ["To the south, dense woodlands stretch as far as the eye "
                         "can see.", "An enchanting realm, but one must tread cautiously, for shadows dance amidst "
                         "the trees."]],
                        ["What about the western reaches? Have you ventured there?", ["Nay, brave one. The west remains"
                         " a mystery to me. My journey has yet to unveil the secrets concealed in those unexplored"
                         " lands.", "Perhaps one day, the winds of fate will carry me in that direction."]],
                        ["Leave", ["May the spirits guide your way, brave traveler."]]],
                       [], [0, 0, 0, 0, 0]],
    "traveler elinor": [["Alas, the city gates remain closed to me. But fear not, fellow wanderer!", "To the east "
                         "lies the charming fishing village of Aquiri. A quaint haven where the sea breeze dances "
                         "with the scent of salt and adventure.", "Seek refuge there, share tales with the fishermen,"
                         " and who knows, perhaps your path will intertwine with the whims of destiny. May the winds"
                         " guide your steps, for there is always another path to tread."], [], [], [0]],
    "traveler kaelin": [["Hail, fellow wanderer. I've treaded the southern realms, through the treacherous "
                         "Dark Forest.", "A word of caution, brave soul – the woods conceal more than beauty. Dark "
                         "whispers and lurking dangers await. I'd advise against venturing there unless your "
                         "courage knows no bounds.", "May your travels be safer than mine, and the path you choose "
                         "be bathed in the light of wisdom."],
                         [], [], [0]],
    "traveler seraph": [["Ah, greetings, fellow wayfarer! Stuck, just like me, eh? Gorrick here mentioned some caves "
                         "to the north that might lead us across.", "Aye, those caves are an option, but beware! "
                         "Lately, they've become a haven for Goblins and other foul creatures.", "A perilous journey "
                         "awaits, my friend. Tread carefully if you choose that path."],
                        [], [], [0]],
    "traveler sylas": [["Greetings, wanderer. A word of wisdom for your journey: always embrace exploration.",
                        "Hidden wonders and untold tales await those who venture beyond the familiar. May your "
                        "steps be guided by curiosity, and may the world unveil its mysteries before you."],
                       [], [], [0]],
    "traveler thaldir": [["Greetings, seeker of fortune. Remember, in every step, 'tis wise to look around and check. "
                          "Secrets often hide where the eye does not linger.", "May the journey unveil the unseen, "
                          "brave one."],
                          [], [], [0]],
    "worker gorrick": [["Hail, traveler! The path ahead is blocked, and only through my efforts can it be opened. Alas,"
                        " it'll take time.", ],
                       [], [], [0]]
}
