# Imports.
# Local imports.
import copy

from ..actions.talk import talk
from .. import displays
from ..enums import PlayerStatus
from ..events.definitions import *
from ..events.timer import Timer
from ..inventory import Inventory
from ..map import Map
from ..player import Player
from .. import utils
from ..world import *

# External imports.
# import pickle
import attrs
import difflib
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

    # Veylan quests/events.
    if is_quest_completed(player=player, quest_id="quest_explore_veylan"):
        event_completed_quest_complete_explore_veylan.execute(player=player, mapgame=mapgame)

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
    player.reinit_after_death()

    for biome in mapgame.map_settings.values():
        biome.reinit_items_now()


def repair(player: Player, mapgame: Map):
    place = mapgame.place_from_list(place_list=[(25, 24), "cave_entrance", "cave_pit", "cave_basin", "cave_gallery",
                                                "cave_passageway_exit", "chimney"])
    place.leave_entry = mapgame.map_settings[(31, 24)]
    player.set_place(place=mapgame.map_settings[(31, 24)])


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


def get_attrs(obj):
    if attrs.has(obj.__class__):
        return {
            f.name: getattr(obj, f.name)
            for f in attrs.fields(obj.__class__)
        }
    return vars(obj)


def quick_migrate(old_object: object, new_object: object) -> None:
    RENAMED_ATTRS = {}

    old_attrs = get_attrs(old_object)
    new_attrs = get_attrs(new_object)
    new_attr_names = list(new_attrs.keys())

    for name, value in old_attrs.items():
        if name in new_attrs:
            setattr(new_object, name, value)
            continue

        new_name = RENAMED_ATTRS.get(name)
        if new_name and new_name in new_attrs:
            setattr(new_object, new_name, value)
            continue

        matches = difflib.get_close_matches(
            name, new_attr_names, n=1, cutoff=0.75
        )
        if matches:
            setattr(new_object, matches[0], value)


def update_game(player: Player,
                mapgame: Map,
                option: str) -> str:
    """
    Updates class Player and class Map.
    """
    # Map updates.
    if option == "map_all":
        mapgame.items = copy.deepcopy(ITEMS)
        # mapgame.quests = copy.deepcopy(QUESTS)
        # mapgame.npcs = copy.deepcopy(NPCS)
        # mapgame.biomes = copy.deepcopy(BIOMES)
        # mapgame.entries = copy.deepcopy(ENTRIES)
        mapgame.fishes = copy.deepcopy(FISHES)
        mapgame.mobs = copy.deepcopy(MOBS)

        for biome in mapgame.map_settings.values():
            biome.reset_mobs(force_respawn=True)

        for entrie in mapgame.entries.values():
            entrie.reset_mobs(force_respawn=True)

        return "Dream map was all updated."

    if option == "map_npcs":
        mapgame.npcs = copy.deepcopy(NPCS)
        return "Dream NPCS MAP updated."

    if option == "map_mobs":
        mapgame.mobs = copy.deepcopy(MOBS)
        return "Dream MOBS MAP updated."

    if option[:3] == "npc":
        mapgame.npcs[option[4:]] = copy.deepcopy(NPCS[option[4:]])
        return f"Npc {mapgame.npcs[option[4:]].name.title()} updated."

    if option == "player":
        # All attributes.
        new_player = Player(name=player.name,
                            place=player.place,
                            last_place=player.last_place,
                            last_entry=player.last_entry,
                            inventory=player.inventory,
                            skills=[SKILLS["attack"]])
        quick_migrate(old_object=player, new_object=new_player)
        player = new_player

        # Skills.
        updated_skills = []
        for skill in player.skills:
            updated_skills.append(SKILLS[skill.id])
        player.skills = updated_skills

        return "Dream of Player was updated."

    return "Nothing done."
