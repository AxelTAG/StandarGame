# Imports.
# Locals imports.
from . import globals

from .biome import Biome
from .enums import Months, Directions
from .map import Map
from .mob import Mob
from .player import Player
from .utils import clear, patron_print, text_2_col, text_ljust, typewriter, underscores

INPUT_LABEL = " " * 4 + "# "
INPUT_LABEL_BATTLE = " # "
ITEM_SPACING = " " * 6
PAUSE_LABEL = " > "
PLAYER_LVL_UP_MSG = "You have lvl up. ASSIGN Strength/Agility/Vitality. You can assign 3 points."


def disp_assign(st: int) -> str:
    return f"Assign skill point ({st}) to: \n- Strength (STR)\n- Agility (AGI)\n- Resistance (RES)\n- Vitality (VIT)"


def disp_attack() -> str:
    return "Use ATTACK ENEMY to attack an enemy."


# Bar display
def disp_line(n: int = 18, disp: bool = True) -> str:
    text = "--" + "-" * n + "--"
    if disp:
        print(text)
    return text


# Battle display.
def disp_battle(players: list[Player],
                enemies: list[Mob],
                screen: str,
                width: int = 36) -> None:
    clear()
    disp_title()
    disp_game_label()

    length = max(len(players), len(enemies))

    cmp_text = []
    cmp_text = cmp_text + text_2_col(msg1=disp_line(width - 4, disp=False),
                                     msg2=disp_line(width - 4, disp=False),
                                     width=width,
                                     ch="-")
    for i in range(length):
        cmp_text += text_2_col(msg1=disp_info(entitie=mock_list_length(ls=players, length=length)[i], onbattle=True),
                               msg2=disp_info(entitie=mock_list_length(ls=enemies, length=length)[i], onbattle=True),
                               width=width,
                               ch="|")
        cmp_text = cmp_text + text_2_col(msg1=disp_line(width - 4, disp=False),
                                         msg2=disp_line(width - 4, disp=False),
                                         width=width,
                                         ch="+")

    cmp_text = cmp_text + text_2_col(msg1=disp_player_battle_actions(player=players[0]),
                                     msg2=screen,
                                     width=width,
                                     ch="|")
    cmp_text = cmp_text + text_2_col(msg1=disp_line(width - 4, disp=False),
                                     msg2=disp_line(width - 4, disp=False),
                                     width=width,
                                     ch="-")

    # Display.
    disp_list(list_to_display=cmp_text, prefix=" ")


# Disp use.
def disp_use() -> str:
    return "USE -ITEM"


# Disp drop.
def disp_drop() -> str:
    return "DROP -QUANTITY -ITEM."


def disp_enemies(enemies: list[Mob], display: bool = True, prefix: str = " ", subfix: str = "") -> list[str] | None:
    labels = [f" {prefix}{i} - {enemy.name.upper()}{subfix}" for i, enemy in enumerate(enemies, 1)]
    if display:
        print(f"\n{prefix}SELECT ENEMY:{subfix}")
        for label in labels:
            print(label)
    return labels


# Enter action.
def disp_enter(place: Biome) -> str:
    if place.entries:
        msg = "You want to ENTER TO:"
        n = 0
        for entrie_key, entrie in place.entries.items():
            if type(entrie) == Biome or entrie.hide["visibility"]:
                entrie_name = " ".join(entrie_key.split("_")).title()
                msg += f"\n - {entrie_name}"
                n += 1
            else:
                continue
        if n < 1:
            return "There aren't entries here."
        return msg
    else:
        return "There aren't entries here."


# Equip display.
def disp_equip(equip: dict) -> str:
    text = "EQUIP:"
    for body_part, item in equip.items():
        body_part_name = body_part.name.replace('_', ' ').title()

        if equip[body_part] is not None:
            text += f"\n- {body_part_name}: {item.name}."
        else:
            text += f"\n- {body_part_name}: None."
    return text


def disp_game_label() -> None:
    print(" < GAME >")
    print()


def disp_game_loss() -> None:
    print()
    print("    YOU HAVE DIED")
    print("    LOST DREAM")
    input("    > ")


def disp_bar(current_value: int, max_value: int, width: int = 25) -> str:
    hits = int(width * (current_value / max_value))
    no_hits = width - int(width * (max(current_value, 0) / max_value))
    hpbar = "|" + "█" * hits + "-" * no_hits + "|"
    return hpbar


def disp_info(entitie: Player | Mob, onbattle: bool = False) -> str:
    if entitie is None:
        return ""
    text_info = ""
    text_info += entitie.name.upper()
    text_info += f"\n HP: {int(entitie.hp)} / {entitie.hpmax}"
    text_info += f"\n {disp_bar(current_value=entitie.hp, max_value=entitie.hpmax, width=25)}"
    if entitie.has_vital_energy():
        text_info += f"\n VITAL ENERGY: {int(entitie.vital_energy)} / {entitie.vital_energy_max}"
        text_info += f"\n {disp_bar(current_value=entitie.vital_energy, max_value=entitie.vital_energy_max, width=25)}"
    text_info += f"\n{disp_statuses(entitie=entitie, onbattle=onbattle)}"
    text_info += f"\n ATTACK: {int(entitie.attack)}"
    return text_info


def disp_intro(width: int = 60) -> None:
    disp_logo(width=width)
    print(" < PRESS ENTER > ".center(width))


def disp_player_battle_actions(player: Player,
                               prefix: str = "",
                               subfix: str = "",
                               display: bool = False) -> str:
    _, labels = player.get_available_actions(onbattle=True)
    actions = []
    for i, label in enumerate(labels):
        actions.append(f"{prefix}{i} - {label.upper()}{subfix}")
        if display:
            print(f"{prefix}{i} - {label.upper()}{subfix}")
    return "\n".join(actions)


def disp_player_play_actions(player: Player,
                             mapgame: Map,
                             prefix: str = "",
                             subfix: str = "",
                             display: bool = False) -> str:
    # Moves.
    moves = mapgame.get_avaible_moves(player=player)
    moves_labels = []
    for i, move in enumerate(moves, 1):
        if i == 1:
            x_pos, y_pos = player.x, player.y - 1
        elif i == 2:
            x_pos, y_pos = player.x + 1, player.y
        elif i == 3:
            x_pos, y_pos = player.x, player.y + 1
        elif i == 4:
            x_pos, y_pos = player.x - 1, player.y
        else:
            x_pos, y_pos = player.x, player.y
        biome_name = player.get_biome_label(x=x_pos, y=y_pos)
        if move:
            moves_labels.append(f"{i} - {Directions(i).name} ({biome_name})")

    # Actions.
    _, actions_labels = player.get_available_actions(onbattle=False)

    actions = [f"{prefix}{0} - {actions_labels[0].upper()}{subfix}"]

    for i, label in enumerate(moves_labels):
        actions.append(f"{prefix}{label.upper()}{subfix}")
        if display:
            print(f"{prefix}{label.upper()}{subfix}")
    for i, label in enumerate(actions_labels[1:], 5):
        actions.append(f"{prefix}{i} - {label.upper()}{subfix}")
        if display:
            print(f"{prefix}{i} - {label.upper()}{subfix}")
    return "\n".join(actions)


def disp_show_list_items(player: Player, items: dict, player_quantity: bool = False) -> tuple[list, list]:
    print()
    items_list, prices_list, n, item_stock = [], [], 0, ""
    for item_key, item_v in items.items():
        item_name = underscores(text=item_key, delete=True).title()
        if player_quantity:
            item_stock = f" [{player.inventory.items[item_key]}]"
        print(
            f"{ITEM_SPACING}{n + 1}) {item_name}{item_stock}: {', '.join([f'{q.title()} {r}' for q, r in item_v.items()])}.")

        items_list.append(item_key)
        prices_list.append(item_v)
        n += 1

    print(f"{ITEM_SPACING}{n + 1}) Quit.")
    print()
    print(f"{ITEM_SPACING}[GOLD: {player.inventory.gold}]\n")

    return items_list, prices_list


def disp_show_options(game):
    clear()
    disp_title()
    print(" < OPTIONS >")
    print()
    print(" 1 - MUSIC VOLUME")
    print(" 0 - QUIT")
    print()


def disp_skill_selection(entitie: Player | Mob, prefix: str = "", subfix: str = "") -> None:
    print()
    print(f"{prefix}SELECT THE SKILL: ")
    for i, skill in enumerate(entitie.skills, 0):
        if skill.id != "attack":
            print(f"{prefix}{i} - {skill.name.upper()} (COST {skill.cost} VT){subfix}")


def disp_list(list_to_display: list, prefix: str = "", subfix: str = "", patron: list = None) -> None:
    if patron is not None:
        for i, line in enumerate(list_to_display):
            print(prefix + patron[i] + line + patron[i] + subfix)
        return

    for line in list_to_display:
        print(prefix + line + subfix)


def disp_load_game() -> None:
    print(" < LOAD DREAM >")
    print()


def disp_logo(width: int = 80) -> None:
    logo = """
                                             #   
                              ++    ######   
                   #      +#   ##########    
                 ##     #- +#############    
                ###  ## .#####   -#######    
               #########                #    
               -####### #########            
              -########  ################    
              #######   #    ############    
             ######## ####  #   #######      
            ########  #######     ###        
          ######    ## #########    #        
      ######     ###  # ##########           
  #######   #########    ########            
 ####+    ############+   ####               
 ###  .################   ##                 
  #   ##################                     
  #  ######+######                           
 -  #+                                       
 """
    logo_lines = logo.split(sep="\n")
    for line in logo_lines:
        print(line.center(width))


def disp_main_screen():
    print(" < MENU >")
    print()
    print(" 1 - NEW DREAM")
    print(" 2 - LOAD DREAM")
    print(" 3 - RULES")
    print(" 4 - OPTIONS")
    print(" 0 - QUIT")
    print()


def disp_narration(narration: list[str] = None, speed: float = 0.3) -> None:
    for _ in range(2):
        clear()
        disp_title()
        print("\n" * 2)
        print("    ")
        if narration is None:
            typewriter(text=f". . .", speed=speed, previous_text=" " * 4)
            return
    for line in narration:
        typewriter(text=line, speed=speed)


def disp_new_game(existent_player: Player = None) -> None:
    if existent_player is None:
        print(" < NEW DREAM >")
        print()
    else:
        print(" < NEW DREAM >")
        print()
        print(" There is already a dream existing, do you want to delete it?")
        print()
        print(f" NAME: {existent_player.name} / LVL: {existent_player.level}")
        print()
        print(" 1 - Yes")
        print(" 2 - No")
        print()


# Look around action.
def disp_look_around(place: Biome) -> str:
    items = place.get_items()
    mobs = place.mobs_respawned
    trees = place.get_trees_respawned()

    if not any([bool(items), bool(mobs), bool(trees)]):
        return "Nothing special here."

    text = "You have looked around and found:"
    if items:
        for item in items:
            text += "\n - " + item.replace("_", " ").title() + "."

    if mobs:
        for mob in mobs:
            text += "\n - " + mob.name.title() + "."

    if trees:
        for tree in trees:
            text += "\n - " + tree.name.title() + "."

    return text


# Play display.
def disp_play(player: Player,
              mapgame: Map,
              screen: str,
              width: int) -> None:

    text1 = disp_play_location_and_time(player=player, mapgame=mapgame, prefix="", subfix="")
    text2 = player.place.get_description(month=mapgame.current_month)
    text3 = disp_play_info(player=player)
    text41 = disp_play_prim_stats(player=player, width=width // 2 - 2)
    text42 = disp_play_sec_stats(player=player, width=width // 2 - 2)
    text4 = "\n".join(text_2_col(text41, text42, int(width / 2 - 2), "|", False))
    text5 = disp_player_play_actions(player=player, mapgame=mapgame)
    text6 = screen

    fixture_text = []
    fixture_text += text_2_col(disp_line(width - 4, disp=False), disp_line(width - 4, disp=False), width, "-")
    fixture_text += text_2_col(text1, text2, width, "|")
    fixture_text += text_2_col(disp_line(width - 4, disp=False), disp_line(width - 4, disp=False), width, "+")
    fixture_text += text_2_col(text3, text4, width, "|", False)
    fixture_text += text_2_col(disp_line(width - 4, disp=False), disp_line(width - 4, disp=False), width, "+")
    fixture_text += text_2_col(text5, text6, width, "|")
    fixture_text += text_2_col(disp_line(width - 4, disp=False), disp_line(width - 4, disp=False), width, "-")

    # Displays.
    disp_play_header(length=23,
                     display=True)
    disp_list(list_to_display=fixture_text,
              patron=patron_print(elements=globals.PATRON, n=len(fixture_text)))


def disp_play_header(length: int, display: bool = True) -> None:
    if display:
        print(" " + ".--." * length + " ")
        print("/ " + ".. \\" * length)
        print("\\ \\/" + "\\ `'" * (length - 2) + "\\ \\/ /")
        print(" \\/ /" + "`--'" * (length - 2) + "\\/ / ")


def disp_play_tale(length: int, display: bool = True) -> None:
    if display:
        print(" / /\\" + ".--." * (length - 2) + "/ /\\ ")
        print("/ /\\ " + "\\.. " * (length - 2) + "\\/\\ \\")
        print("\\ `'" * length + " /")
        print(" " + "`--'" * length + " ")


def disp_play_location_and_time(player: Player, mapgame: Map, prefix: str = "", subfix: str = "") -> str:
    location = f"LOCATION: {player.place.get_name(month=mapgame.current_month).upper()}"
    region = f"REGION: {mapgame.get_region_name(x=player.x, y=player.y)}"
    coordinates = f"COORD: {player.x} {player.y}"
    time_of_day = f"TIME OF DAY: {mapgame.current_time_of_day_name.upper()} [{mapgame.hour}HS]"
    week_day = f"WEEK DAY: {mapgame.current_week_day_name.upper()} [{mapgame.day} DAY]"
    month_year = f"MONTH: {Months(mapgame.month).name.upper()} - YEAR: {mapgame.year}"

    return "\n".join([location, region, coordinates, time_of_day, week_day, month_year])


def disp_play_info(player: Player) -> str:
    name = f"NAME: {player.name.upper()}"
    exp_level = f"EXP: {player.exp}/{player.expmax} | LVL: {player.level}"
    exp_bar = disp_bar(current_value=player.exp, max_value=player.expmax, width=18)
    hp = f"HP: {player.hp} / {player.hpmax}"
    hp_bar = f"{disp_bar(current_value=player.hp, max_value=player.hpmax, width=30)}"

    vt, vt_bar = "", ""
    if player.has_vital_energy():
        vt = f"VITAL ENERGY: {int(player.vital_energy)} / {player.vital_energy_max}"
        vt_bar = f"{disp_bar(current_value=player.vital_energy, max_value=player.vital_energy_max, width=25)}"

    statuses = disp_statuses(entitie=player, onbattle=False)
    gold = f"GOLD: {player.get_gold()}"

    info_line = [name, exp_level, exp_bar, hp, hp_bar, vt, vt_bar, statuses, gold]
    return "\n".join([info for info in info_line if info])


def disp_play_prim_stats(player: Player, width: int) -> str:
    title = "PRIM. STATS:\n"
    attack = twotext_justify(title="ATTACK:", number=f"{int(player.attack)}", width=width)
    defense = twotext_justify(title="DEFENSE:", number=f"{int(player.defense)}", width=width)
    evasion = twotext_justify(title="EVASION:", number=f"{int(player.evasion * 100)}%", width=width)
    precision = twotext_justify(title="PRECISION:", number=f"{int(player.precision * 100)}%", width=width)
    weight = twotext_justify(title="WEIGHT:",
                             number=f"{int(player.current_weight)}/{int(player.weight_carry)}",
                             width=width)

    info_line = [title, attack, defense, evasion, precision, weight]
    return "\n".join([info for info in info_line if info])


def disp_play_sec_stats(player: Player, width: int) -> str:
    title = "SEC. STATS:\n"
    strength = twotext_justify(title="STRENGTH:", number=f"{int(player.strength)}", width=width)
    resistance = twotext_justify(title="RESISTANCE:", number=f"{int(player.resistance)}", width=width)
    agility = twotext_justify(title="AGILITY:", number=f"{int(player.agility)}", width=width)
    dexterity = twotext_justify(title="DEXTERITY:", number=f"{int(player.dexterity)}", width=width)
    vitality = twotext_justify(title="VITALITY:", number=f"{int(player.vitality)}", width=width)

    info_line = [title, strength, resistance, agility, dexterity, vitality]
    return "\n".join([info for info in info_line if info])


def disp_read(entitie: str) -> None:
    pass


def disp_rules() -> None:
    print()
    print()
    print(" < RULES >")
    print()
    print(" I am the creator of this dream story and these are the rules.")
    print()
    print(" 1) Follow your path.")
    print(" 2) Trace your path with: 'map' and 'draw map'.")
    print(" 3) Many actions are allowed ('use', 'enter', 'talk', 'look around', etc.), \n"
          "    and others you'll have to discover along your journey.")
    print(" 4) Remember: sleeping in a bed, will charge your energy.")
    print()


# Show inventory display.
def disp_show_inventory(player: Player):
    text = "INVENTORY:"
    for item in player.inventory.get_item_objects:
        text += f"\n - {item.name}: {player.get_item_quantity(item=item)}"
    text += f"\n - Gold: {player.get_gold()}"
    return text


# Sleep options display.
def disp_sleep(place: Biome) -> str:
    if "bed" in place.get_items():
        return "You want to sleep to: \n- Sleep to Morning\n- Sleep to Afternoon\n- Sleep to Evening\n- Sleep to Night"
    else:
        return "There is no bed here."


def disp_statuses(entitie: Player | Mob, onbattle: bool = False) -> str:
    statuses_list = []
    statuses = entitie.statuses + entitie.statuses_saved if onbattle else entitie.statuses

    for status in statuses:
        statuses_list.append(f"{status.name.upper()}")
        if status.is_damaging():
            statuses_list[-1] += f" [{status.stacks}]"
        if status.is_sttuner() or status.is_paralyzer():
            if onbattle:
                statuses_list[-1] += f" [{status.duration + 1}]"
            if not onbattle:
                statuses_list[-1] += f" [{status.duration}]"

    if not onbattle:
        if entitie.hungry <= 10:
            statuses_list.append(f"HUNGRY")
        if entitie.thirsty <= 10:
            statuses_list.append(f"THIRSTY")

    if not statuses_list:
        statuses_list.append(f"HEALTHY")

    return f"STATUS: {' '.join(statuses_list)}"


# Talk npc options.
def disp_talk(place: Biome, mapgame: Map) -> str:
    if place.get_npc():
        msg = "You want to talk to:"
        for i, npc in enumerate(place.get_npc()):
            warning = ""
            if mapgame.npcs[npc].has_quest():
                warning = " [!]"
            msg += f"\n - {npc.replace('_', ' ').title()}{warning}"
        return msg
    else:
        return "No one is here."


def disp_talk_answers(answers):
    print()
    for i in range(len(answers.keys())):
        print(" " * 4 + str(i + 1), ") " + answers[i + 1].capitalize() + ".")
    print(" " * 4 + str(len(answers) + 1), ") Leave.")
    print()


# Talk display.
def disp_standard_head(name: str) -> None:
    clear()
    disp_title()
    print(" < GAME >")
    print()
    print(" " * 4 + name.title() + ":", end="\n ")
    print()


# Talk printing function.
def disp_standard_tw(name: str, message: list):
    clear()
    # Printing of message.
    for line in message:
        disp_standard_head(name)

        lines = text_ljust(line, width=70)
        for text in lines:
            typewriter(" " * 4 + text)
            print()

        input(" " * 4 + "> ")


# Title display.
def disp_title() -> None:
    title = ["  ___  ____|___|_________     ____|_____ ___                     ",
             " | ' ||    |   |___/___|_)        |__|__| ' |                    ",
             "\n",
             "  ___ ____ ____  ___  .-. _____       _  ________ ____/ ___ ____ ",
             " (   )_/(_)__|_)(   )(   )___/_    (_/ )|    __|_)    \\| ' |_/(_)",
             "  `-'            `|   `-'                                        "]
    print()
    for line in title:
        print(line)
    print()
    print()


# Wait options display.
def disp_wait() -> str:
    return "You want to wait to:\n- Wait to Morning\n- Wait to Afternoon\n- Wait to Evening\n- Wait to Nigth"


def equal_len(ls1: list, ls2: list, refill=None) -> tuple[list, list]:
    if ls1 is None:
        ls1 = []
    if ls2 is None:
        ls2 = []
    max_len = max(len(ls1), len(ls2))
    while len(ls1) < max_len:
        ls1.append(refill)
    while len(ls2) < max_len:
        ls2.append(refill)
    return ls1, ls2


def mock_list_length(ls: list, length: int) -> list:
    return ls + [None] * (length - len(ls))


def get_max_text_length(texts: list) -> int:
    return max(map(max, texts))


def twotext_justify(title: str, number: str, width: int) -> str:
    title_length = len(title)
    number_length = len(number)

    if title_length + number_length > width:
        return f"{title} {number}"

    spaces = width - title_length - number_length
    return f"{title}{' ' * spaces}{number}"
