WHITE = (255, 255, 255, 255)

DAY_PARTS = ("MORNING", "AFTERNOON", "EVENING", "NIGHT")

BIOMS = {
    "canyon": {
        "t": "CANYON",
        "e": False,
        "e_list": ["goblin", "orcs"],
        "e_chance": [80, 50],
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
        "e_list": ["slime"],
        "e_chance": [30],
        "r": [],
        "d": "Seaside with swaying palm trees, echoing waves, and vibrant life.",
        "c": (239, 228, 176, 255)},
    "fields": {
        "t": "FIELDS",
        "e": False,
        "e_list": ["slime"],
        "e_chance": [30],
        "r": ["walk"],
        "d": "Nothing important.",
        "c": (255, 255, 255, 255)},
    "forest": {
        "t": "FOREST",
        "e": True,
        "e_list": ["slime"],
        "e_chance": [30],
        "r": ["walk"],
        "d": "Thick trees, vibrant flora, wildlife, hidden trails, and lurking danger in this treacherous "
             "forest realm.",
        "c": (34, 177, 76, 255)},
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
        "e_list": ["goblin"],
        "e_chance": [30],
        "r": ["walk"],
        "d": "Nothing important.",
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
        "e_list": ["slime"],
        "e_chance": [10],
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
        "e_list": ["goblin", "slime"],
        "e_chance": [30, 30],
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
        "e": False,
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
        "d": "Nothing important.",
        "c": (167, 167, 167, 255)},
    "workers": {
        "t": "WORKERS",
        "e": True,
        "e_list": [""],
        "e_chance": [0],
        "r": ["walk"],
        "d": "Nothing important.",
        "c": (163, 73, 164, 255)},
    }

# MAP SETTING format [x, y, objects, description].
MAP_SETTING = {
    (0, 0): [["bed"], "Island hut, a cozy retreat adorned with a bed, a table, two chairs, and a window, "
                      "invites serenity amid nature's whispers."],
    (2, 1): [["boat"], "Seaside with anchored boat, echoing waves and vibrant coastal life."],
    (6, 2): [["boat"], "Seaside with anchored boat, echoing waves and vibrant coastal life."],
    (10, 5): [["walk"], "Southern gateway, welcoming gates, cobblestone paths, and a charming, serene atmosphere "
                        "greet visitors."],
    (15, 5): [["wings"], "Seaside with anchored boat, echoing waves and vibrant coastal life."],
}
