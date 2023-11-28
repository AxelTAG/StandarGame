# Command line settings.
WIDTH = 92
HEIGHT = 40

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

# MOBS.
MOBS = {
    "goblin": {
        "hp": 15,
        "at": 3,
        "go": 8,
        "exp": 3
    },
    "orc": {
        "hp": 20,
        "at": 6,
        "go": 18,
        "exp": 5,
    },
    "slime": {
        "hp": 20,
        "at": 2,
        "go": 12,
        "exp": 2
    },
    "dragon": {
        "hp": 100,
        "at": 8,
        "go": 100
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
    "(2, 1)": {
        "t": "COAST",
        "e": True,
        "e_list": ["slime"],
        "e_chance": [30],
        "r": ["walk"],
        "d": "Seaside with anchored boat, echoing waves and vibrant coastal life. A solitary figure stands at the "
             "water's edge, gazing out into the vastness of the sea, captivated by the rhythmic dance of the waves and "
             "the boundless horizon stretching before them.",
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
        "d": "Seaside with anchored boat, echoing waves and vibrant coastal life.",
        "items": ["boat"],
        "npc": ["captain zelian"],
        "entries": [],
        "c": (239, 228, 176, 255)},
    "(9, 4)": {
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
        "npc": [],
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
        "c": (195, 195, 195, 255)}
}


# NPCs.
NPC = {
    "captain zelian": [["Ah, the sea, a fickle friend and fierce foe.", "Many a ship I've sailed, battling monsters "
                        "and discovering uncharted isles. The ocean whispers secrets to those who listen.", "Legend "
                        "speaks of a mystical realm beneath these waves, hidden from mortal eyes.", "One day, perhaps, "
                        "the tides will reveal its mysteries to a brave soul like yourself, adventurer."]],
    "mayor thorian": [["Greetings, traveler, to our humble abode! Epiiat is open to all seeking refuge.", "However, I "
                       "must caution you—recently, the once-tranquil caves to the north have become infested with "
                       "Goblins and other nefarious beings.", "We fear a sinister leader guides them.", "Be vigilant on "
                       "your journey through our beloved town and beyond, and may the Goddesses guide your steps."]],
    "traveler seraph": [["Ah, greetings, fellow wayfarer! Stuck, just like me, eh? Gorrick here mentioned some caves "
                         "to the north that might lead us across.", "Aye, those caves are an option, but beware! "
                         "Lately, they've become a haven for Goblins and other foul creatures.", "A perilous journey "
                         "awaits, my friend. Tread carefully if you choose that path."]],
    "worker gorrick": [["Hail, traveler! The path ahead is blocked, and only through my efforts can it be opened. Alas,"
                        " it'll take time.", ]]
}
