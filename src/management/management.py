# Imports.
# Local imports.
from ..actions.talk import talk
from .. import displays
from ..events.definitions import *
from ..events.timer import Timer
from ..map import Map
from ..player import Player
from .. import utils
from ..world import *

# External imports.
# import pickle
import dill as pickle
from datetime import datetime


def is_quest_started(player: Player, quest_id: str) -> bool:
    quest = player.get_quest(quest=quest_id, in_progress=True, completed=False)
    if quest is None:
        return False
    return quest.is_started()


def is_quest_completed(player: Player, quest_id: str) -> bool:
    quest = player.get_quest(quest=quest_id, in_progress=True, completed=False)
    if quest is None:
        return False
    return quest.is_completed()


def is_quest_rewarded(player: Player, quest_id: str) -> bool:
    quest = player.get_quest(quest=quest_id, in_progress=True, completed=True)
    if quest is None:
        return False
    return quest.is_rewarded()


# Event handler.
def event_handler(player: Player,
                  mapgame: Map,
                  time_init: datetime) -> tuple[int, int]:
    # Player sea trap.
    if player.status not in player.place.get_status(month=mapgame.current_month):
        player.hp = 0
        return False, True

    # Quest/Event control
    # Starter quests/events.
    if is_quest_completed(player=player, quest_id="quest_exit_the_hut"):
        event_completed_exit_the_hut.execute(player=player, mapgame=mapgame)

    if is_quest_completed(player=player, quest_id="quest_eat_soup"):
        event_completed_eat_soup.execute(player=player, mapgame=mapgame)

    if is_quest_completed(player=player, quest_id="quest_find_loial"):
        event_completed_find_loial.execute(player=player, mapgame=mapgame)

    if is_quest_started(player=player, quest_id="quest_deliver_wood"):
        event_started_find_loial.execute(player=player, mapgame=mapgame)

    if is_quest_completed(player=player, quest_id="quest_deliver_wood"):
        event_completed_deliver_wood.execute(player=player, mapgame=mapgame)

    if is_quest_started(player=player, quest_id="slime_slayer_I"):
        event_completed_slime_slayer_I.execute(player=player, mapgame=mapgame)

    if is_quest_rewarded(player=player, quest_id="slime_slayer_II"):
        event_rewarded_slime_slayer_II.execute(player=player, mapgame=mapgame)

    # Epiiat quests/events.
    event_goblin_chief_battle.execute(player=player, mapgame=mapgame)

    if is_quest_rewarded(player=player, quest_id="quest_goblin_chief"):
        event_rewarded_goblin_chief.execute(player=player, mapgame=mapgame)

    # Aquiri quests/events.
    if is_quest_started(player=player, quest_id="quest_marlin_fish_for_brann"):
        event_started_quest_marlin_fish_for_brann.execute(player=player, mapgame=mapgame)

    if is_quest_completed(player=player, quest_id="quest_marlin_fish_for_brann"):
        event_completed_quest_marlin_fish_for_brann.execute(player=player, mapgame=mapgame)

    if is_quest_completed(player=player, quest_id="quest_find_caravan_leader_darek"):
        event_completed_quest_find_caravan_leader_darek.execute(player=player, mapgame=mapgame)

    if is_quest_completed(player=player, quest_id="quest_destroy_rocks_on_valley"):
        event_completed_quest_destroy_rocks_on_valley.execute(player=player, mapgame=mapgame)

    if is_quest_completed(player=player, quest_id="quest_gareth_deliver"):
        event_completed_quest_gareth_deliver.execute(player=player, mapgame=mapgame)

    # FireFrost first encounter quests/events.
    event_firefrost_first_encounter_battle.execute(player=player, mapgame=mapgame)

    if is_quest_completed(player=player, quest_id="quest_firefrost_first_encounter"):
        event_completed_quest_firefrost_first_encounter.execute(player=player, mapgame=mapgame)

    return True, False


def import_player(path: str) -> Player | None:
    try:
        with open(path, 'rb') as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:
        return None


def import_map(path: str) -> Map | None:
    try:
        with open(path, 'rb') as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:
        return None


def map_control_handling(player: Player,
                         mapgame: Map):
    # Control of Innkeeper room expirations.
    for npc in player.place.get_npc():
        if mapgame.npcs[npc].npc_type == NpcTypes.INNKEEPER:
            expirated_room_keys = mapgame.check_room_expiration(player=player,
                                                                npc=npc)
            for key in expirated_room_keys:
                player.inventory.drop_item(item=key,
                                           quantity=player.inventory.items[key])
                displays.disp_standard_tw(
                    name=mapgame.npcs[npc].name,
                    message=["Ah, there you are. Your stay was pleasant, I hope. But your days are up, "
                             "traveler. I’ll need the room key back now. Don’t worry—you’re welcome to "
                             "rent it again if you plan on staying longer."])

            for key in expirated_room_keys:
                del mapgame.npcs[npc].room_expirations[key]

    # Sailor Kael detention.
    if "sailor_kael" in player.place.get_npc() and player.place == mapgame.map_settings[(39, 39)].entries[
        "thornes_ship"]:
        talk(npc=mapgame.npcs["sailor_kael"], player=player, mapgame=mapgame)
        player.set_place(place=player.last_place)

    # Guard Lorian ddetention.
    if "guard_lorian" in player.last_place.get_npc() and player.place == mapgame.map_settings[(24, 41)]:
        quest = player.get_quest("quest_gareth_deliver")
        if quest is None or not quest.is_started():
            talk(npc=mapgame.npcs["guard_lorian"], player=player, mapgame=mapgame)
            player.set_place(place=player.last_place)


def load(path_usavepkl: str = "./save/cfg_save.pkl",
         path_msave: str = "./save/cfg_map.pkl",
         path_hsave: str = "./save/cfg_hash.txt",
         check_hash: bool = True) -> tuple[bool, str, Player | None, Map | None]:
    """Checks corruption of files and finally loads src."""
    if check_hash:
        load_hash = utils.load_dict_from_txt(path_hsave)
        if not utils.get_hash("../../save/cfg_save.pkl") == load_hash["hash"]:
            return False, " Corrupted file.", None, None

    player = import_player(path_usavepkl)
    mapgame = import_map(path_msave)

    if player is None:
        return False, " Player have been not found.", None, None

    if mapgame is None:
        return False, " Player map file have been not found.", None, None

    return True, f" Welcome back {player.name}.", player, mapgame


def reinit(player: Player, mapgame: Map):
    # Player reinit.
    player.hp = int(player.hpmax)
    player.set_place(place=mapgame.map_settings[(player.x_cp, player.y_cp)])
    player.status = 0
    player.poison = 0
    player.hungry = 48
    player.thirsty = 48
    player.exp = 0

    # Map reinit.
    utils.reset_map(ms=mapgame.map_settings,
                    keys=[(14, 25), (18, 26)])


def repair(player: Player, mapgame: Map):
    pass


# Save function.
def save(player: Player,
         mapgame: Map,
         time_init: datetime,
         path_usavepkl: str = "./save/cfg_save.pkl",
         path_mappkl: str = "./save/cfg_map.pkl",
         path_hsave: str = "./save/cfg_hash.txt") -> None:
    """Saves src."""
    player.refresh_time_played(datetime.now(), time_init)

    # Inventory, user stats and map setting saving (export to txt).
    utils.export_player(player, path_usavepkl)
    utils.export_player(mapgame, path_mappkl)

    # Hash saving (export to dict).
    utils.export_dict_to_txt(dictionary={"hash": utils.get_hash(path_usavepkl)}, file_path=path_hsave)


def update(player: Player,
           mapgame: Map,
           option: str) -> tuple[str, Player, Map]:
    """
    Updates class Player and class Map.
    """
    if option == "map_npcs":
        mapgame.npcs = NPCS.copy()
        return "Update NPCS MAP succesfully.", player, mapgame

    if option == "map_mobs":
        mapgame.mobs = MOBS.copy()
        return "Update MOBS MAP succesfully.", player, mapgame

    if option == "player":
        new_player = Player(name=player.name,
                            hp=player.hp,
                            level=player.level,
                            exp=player.exp,
                            expmax=player.expmax,
                            hungry=player.hungry,
                            thirsty=player.thirsty,
                            status=player.status,
                            poison=player.poison,
                            freeze=player.freeze,
                            b_hpmax=player.b_hpmax,
                            b_attack=player.b_attack,
                            b_defense=player.b_defense,
                            b_evasion=player.b_evasion,
                            b_precision=player.b_precision,
                            b_weight_carry=player.b_weight_carry,
                            strength=player.strength,
                            resistance=player.resistance,
                            agility=player.agility,
                            vitality=player.vitality,
                            dexterity=player.dexterity,
                            attack_factor=player.attack_factor,
                            defence_factor=player.defence_factor,
                            evasion_factor=player.evasion_factor,
                            precision_factor=player.precision_factor,
                            vitality_factor=player.vitality_factor,
                            vision=player.vision,
                            x=player.x,
                            y=player.y,
                            x_cp=player.x_cp,
                            y_cp=player.y_cp,
                            outside=player.outside,
                            place=player.place,
                            last_place=player.last_place,
                            last_entry=player.last_entry,
                            st_points=player.st_points,
                            sk_points=player.sk_points,
                            inventory=player.inventory,
                            equip=player.equip,
                            map=player.map,
                            events=player.events,
                            time_played=player.time_played)
        return "Player class updated.", new_player, mapgame

    if option == "map_13_0":
        sub_cave_2_3 = ENTRIES["sub_cave_2_3"]
        sub_cave_3_1 = ENTRIES["sub_cave_3_1"]
        mapgame.map_settings[(25, 24)].entries["big_cave"].entries["passageway_cave_entrance"].entries[
            "goblin_dining_gallery"].entries = {"cave_passageway_entrance": sub_cave_2_3,
                                                "cave_passageway_exit": sub_cave_3_1}
        return "Update MAP 13 0 succesfully.", player, mapgame

    return "Nothing done.", player, mapgame
