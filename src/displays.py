# Imports.
# Locals imports.
from . import globals

from .biome import Biome
from .enums import Months, BodyPart, StatusType
from .map import Map
from .mob import Mob
from .player import Player
from .utils import clear, get_label, patron_print, text_2_col, text_ljust, typewriter, underscores

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
        cmp_text += text_2_col(msg1=disp_info(entitie=mock_length(ls=players, length=length)[i], onbattle=True),
                               msg2=disp_info(entitie=mock_length(ls=enemies, length=length)[i], onbattle=True),
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
    hpbar = "█" * hits + "-" * no_hits + "|"
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
    text_info += disp_statuses(entitie=entitie, onbattle=onbattle)
    text_info += f"\n ATTACK: {int(entitie.attack)}"
    return text_info


def disp_intro(width: int = 60) -> None:
    disp_logo(width=width)
    print(" < PRESS ENTER > ".center(width))


def disp_player_battle_actions(player: Player,
                               prefix: str = "",
                               subfix: str = "",
                               display: bool = False) -> str:
    _, labels = player.get_available_actions()
    actions = []
    for i, label in enumerate(labels):
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


def disp_skill_selection(entitie: Player | Mob, prefix: str = "", subfix: str = "") -> None:
    print()
    print(f"{prefix}SELECT THE SKILL: ")
    for i, skill in enumerate(entitie.skills, 0):
        if skill.id != "attack":
            print(f"{prefix}{i} - {skill.name.upper()} (COST {skill.cost} VT){subfix}")


def disp_list(list_to_display: list, prefix: str = "", subfix: str = "") -> None:
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

    if not items and not mobs:
        return "Nothing special here."

    text = "You have looked around and found:"
    if items:
        for item in items:
            text += "\n - " + item.replace("_", " ").title() + "."

    if mobs:
        for mob in mobs:
            text += "\n - " + mob.name.title() + "."
    return text


# Play display.
def disp_play(player: Player,
              map_game: Map,
              reg: str,
              x: int,
              y: int,
              mdir: list,
              screen_text: str,
              width: int) -> None:
    print("  .--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--. ")
    print(
        " / .. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\.. \\")
    print(
        " \\ \\/\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ `'\\ \\/ /")
    print("  \\/ /`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'\\/ / ")
    t_loc = "LOCATION: " + player.place.get_name(month=map_game.current_month).upper()
    t_reg = "\n REGION: " + reg.upper()
    t_coord = "\n COORD: " + str(x) + " " + str(y)
    t_time = f"\n TIME OF DAY: {map_game.current_time_of_day_name.upper()} [{map_game.hour}HS]"
    t_week_day = f"\n WEEK DAY: {map_game.current_week_day_name.upper()} [{map_game.day} DAY]"
    t_month_year = f"\n MONTH: {Months(map_game.month).name.upper()} - YEAR: {map_game.year}"

    t_name = "NAME: " + player.name.upper()
    t_hp = "\nHP: " + str(int(player.hp)) + "/" + str(player.hpmax)
    t_hpbar = "\n|" + "█" * int(20 * (player.hp / player.hpmax)) + "-" * (
            20 - int(20 * (max(player.hp, 0) / player.hpmax))) + "|"
    t_lvl = "\nEXP: " + str(player.exp) + "/" + str(player.expmax) + " | LVL: " + str(player.level)
    t_expbar = "\n|" + "█" * int(11 * (player.exp / player.expmax)) + "-" * (
            11 - int(11 * (max(player.exp, 0) / player.expmax))) + "|"

    # Status text.
    t_status_types = []
    for status in player.statuses:
        t_status_types.append(f"{status.name.upper()} [{status.stacks}]")
    if player.hungry <= 10:
        t_status_types.append(f"HUNGRY")
    if player.thirsty <= 10:
        t_status_types.append(f"THIRSTY")
    if not t_status_types:
        t_status_types.append(f"HEALTHY")
    t_status = f"\nSTATUS: {' '.join(t_status_types)}"

    # Belt items.
    slot1_item, slot1_quantity = "None", 0
    slot2_item, slot2_quantity = "None", 0
    if player.get_slot_item(slot=0) is not None:
        slot1_item = player.equip[BodyPart.WAIST].slots_packs[0].name
        slot1_quantity = player.get_item_quantity(item=player.equip[BodyPart.WAIST].slots_packs[0])
    if player.get_slot_item(slot=1) is not None:
        slot2_item = player.equip[BodyPart.WAIST].slots_packs[1].name
        slot2_quantity = player.get_item_quantity(item=player.equip[BodyPart.WAIST].slots_packs[1])

    t_gold = f"\nGOLD: {player.inventory.gold}"
    t_item1, t_item2 = "", ""
    if player.equip[BodyPart.WAIST] is not None:
        t_item1 = f"\n5 - {slot1_item.upper()}: {slot1_quantity}"
        t_item2 = f"\n6 - {slot2_item.upper()}: {slot2_quantity}"

    # Text4.1 lines.
    prim_stats = "PRIM. STATS: "
    t_atk = "\n\nATTACK:    " + str(int(player.attack))
    t_def = "\nDEFENSE:   " + str(int(player.defense))
    t_eva = "\nEVASION:   " + str(int(player.evasion * 100)) + "%"
    t_pre = "\nPRECISION: " + str(int(player.precision * 100)) + "%"
    t_weight = "\nWEIGHT:    " + str(int(player.current_weight)) + "/" + str(int(player.weight_carry))

    # Text4.2 lines.
    sec_stats = " SEC. STATS:"
    t_str = "\n\n STRENGTH:   " + str(int(player.strength))
    t_res = "\n RESISTANCE: " + str(int(player.resistance))
    t_agi = "\n AGILITY:    " + str(int(player.agility))
    # t_dex = "\n DEXTERITY:  " + str(int(user["b_dex"]))
    t_vit = "\n VITALITY:   " + str(int(player.vitality))

    text1 = t_loc + t_reg + t_coord + "\n." + t_time + t_week_day + t_month_year
    text2 = player.place.get_description(month=map_game.current_month)
    text3 = t_name + t_lvl + t_expbar + t_hp + t_hpbar + t_status + t_gold
    text41 = prim_stats + t_atk + t_def + t_eva + t_pre + t_weight
    text42 = sec_stats + t_str + t_res + t_agi + t_vit
    text4 = "\n".join(text_2_col(text41, text42, int(width / 2 - 2), "|", False))
    text5 = "0 - SAVE AND QUIT"
    text6 = screen_text

    cmp_text = []
    cmp_text = cmp_text + text_2_col(disp_line(width - 4, disp=False), disp_line(width - 4, disp=False), width, "-")
    cmp_text = cmp_text + text_2_col(text1, text2, width, "|")
    cmp_text = cmp_text + text_2_col(disp_line(width - 4, disp=False), disp_line(width - 4, disp=False), width, "+")
    cmp_text = cmp_text + text_2_col(text3, text4, width, "|", False)
    cmp_text = cmp_text + text_2_col(disp_line(width - 4, disp=False), disp_line(width - 4, disp=False), width, "+")

    for i, status in enumerate(mdir):
        if i == 0:
            x_pos, y_pos = x, y - 1
        elif i == 1:
            x_pos, y_pos = x + 1, y
        elif i == 2:
            x_pos, y_pos = x, y + 1
        elif i == 3:
            x_pos, y_pos = x - 1, y
        else:
            x_pos, y_pos = x, y
        if status:
            text5 += "\n" + globals.DIRECTIONS[i] + " (" + get_label(x_pos, y_pos, player.map).upper() + ")"
    text5 += t_item1 + t_item2

    cmp_text = cmp_text + text_2_col(text5, text6, width, "|")
    cmp_text = cmp_text + text_2_col(disp_line(width - 4, disp=False), disp_line(width - 4, disp=False), width, "-")

    # cmp_text = concatenate_lists(cmp_text, side_text)
    patron = patron_print(globals.PATRON, len(cmp_text))

    for i, line in enumerate(cmp_text):
        print(" " + patron[i] + line + "  " + patron[i])


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
    items = [(item, quantity) for item, quantity in player.inventory.items.items()]
    text = "INVENTORY:"
    for item, quantity in items:
        text += "\n - " + item.replace("_", " ").title() + ": " + str(quantity)
    text += "\n - Gold: " + str(player.inventory.gold)
    return text


# Sleep options display.
def disp_sleep(place: Biome) -> str:
    if "bed" in place.get_items():
        return "You want to sleep to: \n- Sleep to Morning\n- Sleep to Afternoon\n- Sleep to Evening\n- Sleep to Night"
    else:
        return "There is no bed here."


def disp_statuses(entitie: Player | Mob, onbattle: bool = False) -> str:
    statuses_list = []
    for status in entitie.statuses:
        statuses_list.append(f"{status.name.upper()}")
        if status.is_damaging():
            statuses_list[-1] += f" [{status.stacks}]"
        if status.is_sttuner() or status.is_paralyzer():
            statuses_list[-1] += f" [{status.duration}]"

    if onbattle:
        for status in entitie.statuses_save:
            statuses_list.append(f"{status.name.upper()}")
            if status.is_damaging():
                statuses_list[-1] += f" [{status.stacks}]"
            if status.is_sttuner() or status.is_paralyzer():
                statuses_list[-1] += f" [{status.duration}]"

    if not onbattle:
        if entitie.hungry <= 10:
            statuses_list.append(f"HUNGRY")
        if entitie.thirsty <= 10:
            statuses_list.append(f"THIRSTY")

    if not statuses_list:
        statuses_list.append(f"HEALTHY")

    return f"\nSTATUS: {' '.join(statuses_list)}"


# Talk npc options.
def disp_talk(place: Biome, mapgame: Map) -> str:
    if place.get_npc():
        msg = "You want to talk to:"
        for i, npc in enumerate(place.get_npc()):
            msg += "\n - " + npc.replace("_", " ").title()
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


def mock_length(ls: list, length: int) -> list:
    return ls + [None] * (length - len(ls))
