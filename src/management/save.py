# Imports.
# Local imports.
from ..map import Map
from ..player import Player

# External imports.
import pickle
import hashlib
import os
from attrs import define, field
from datetime import datetime, timedelta
from typing import Any


@define
class SaveMetadata:
    """
    Lightweight save information used for displaying an existing game
    in the main menu without loading the full state.

    :ivar player_name: Name of the player character.
    :vartype player_name: str

    :ivar player_level: Current level of the player.
    :vartype level: int

    :ivar play_time: Total accumulated play time.
    :vartype play_time: float

    :ivar player_location: Last known location or region of the player.
    :vartype location: str

    :ivar last_save: ISO-formatted timestamp of the last save.
    :vartype last_save: str
    """
    player_name: str
    player_level: int
    play_time: timedelta
    last_save: str


@define
class SaveGame:
    """
    Full game state container including the Player instance and the Map
    instance. This structure is loaded only when continuing a game.

    :ivar player: Player instance containing all player-related data.
    :vartype player: Any

    :ivar mapgame: Map instance containing the world or region state.
    :vartype game_map: Any

    :ivar timestamp: ISO-formatted timestamp of when the save was created.
    :vartype timestamp: str
    """
    player: Any
    mapgame: Any
    timestamp: str = field(factory=lambda: datetime.now().isoformat())


def assign_value_dict(dictionary: dict, keys: list, value) -> dict:
    current_dict = dictionary
    for key in keys[:-1]:
        current_dict = current_dict[key]

    current_dict[keys[-1]] = value
    return dictionary


def count_first_spaces(string: str) -> int:
    count = 0
    for char in string:
        if char.isspace():
            count += 1
            continue
        break
    return count


def export_dict_to_txt(dictionary: dict, file_path: str) -> None:
    def write_recursive(file, data, depth=0):
        for key, value in data.items():
            if isinstance(value, dict):
                file.write(f"{'  ' * depth}{key}:\n")
                write_recursive(file, value, depth + 1)
            else:
                file.write(f"{'  ' * depth}{key}: {value}\n")

    try:
        with open(file_path, 'w') as doc:
            write_recursive(doc, dictionary)
    except OSError:
        raise OSError("Unable to save the file.")


def get_hash(file_name, algorithm='sha256', block_size=65536):
    hasher = hashlib.new(algorithm)
    with open(file_name, 'rb') as file:
        block = file.read(block_size)
        while len(block) > 0:
            hasher.update(block)
            block = file.read(block_size)
    return hasher.hexdigest()


def load_dict_from_txt(file_path: str) -> dict:
    reloaded_dictionary = {}
    current_key = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if i != 0 and count_first_spaces(lines[i]) < count_first_spaces(lines[i - 1]):
                current_key.pop(-1)
            key, value = line.strip().split(':', 1)
            if value == '':
                current_key.append(key)
                reloaded_dictionary = assign_value_dict(reloaded_dictionary, current_key, {})
            else:
                try:
                    value = eval(value)
                except SyntaxError:
                    value = value.strip()
                except NameError:
                    value = value.strip()
                current_key.append(key)
                reloaded_dictionary = assign_value_dict(reloaded_dictionary, current_key, value)
                current_key.pop(-1)

    return reloaded_dictionary


def load_metadata(filepath: str = "./save/cfg_metadata.pkl") -> SaveMetadata | None:
    """
    Load a :class:`SaveMetadata` instance from file.

    :param filepath: Path to the metadata file.
    :type filepath: str

    :return: Loaded metadata instance.
    :rtype: SaveMetadata
    """
    try:
        with open(filepath, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


def save_metadata(player, filepath: str = "./save/cfg_metadata.pkl") -> None:
    """
    Create and save a :class:`SaveMetadata` object from the current player state.

    The resulting file is lightweight and intended to be loaded quickly
    in the main menu to preview existing saves.

    :param player: Player instance from which metadata will be extracted.
    :type player: Any

    :param filepath: Path where the metadata file will be written.
    :type filepath: str
    """
    metadata = SaveMetadata(
        player_name=player.name,
        player_level=player.level,
        play_time=getattr(player, "time_played", 0.0),
        last_save=datetime.now().isoformat(),
    )

    save_dir = os.path.dirname(filepath)
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)

    with open(filepath, "wb") as f:
        pickle.dump(metadata, f)


def load_game(filepath: str = "./save/cfg_save.pkl",
              filepath_hash: str = "./save/cfg_hash.txt",
              check_hash: bool = True) -> tuple[bool, str, SaveGame | None]:
    """
     Load a full :class:`SaveGame` instance from disk, optionally performing
     an integrity check using a stored hash file. The function returns a tuple
     containing a success flag, a status message, and the loaded save object
     (or ``None`` if loading fails).

     If ``check_hash`` is enabled, the function compares the stored hash value
     against the current hash of the file to validate data integrity. A mismatch
     indicates a corrupted save file and prevents loading.

     :param filepath:
         Path to the serialized ``SaveGame`` file to be loaded.
     :type filepath: str

     :param filepath_hash:
         Path to the text file that stores the expected hash value used
         for integrity validation when ``check_hash`` is ``True``.
     :type filepath_hash: str

     :param check_hash:
         Whether to verify the integrity of the save file using the hash stored
         in ``filepath_hash``. If the hash does not match, the function returns
         an error tuple without attempting to deserialize the save.
     :type check_hash: bool

     :returns:
         A tuple of the form ``(success, message, savegame)`` where:

         - ``success`` (bool): Indicates whether the load operation succeeded.
         - ``message`` (str): Human-readable status or error message.
         - ``savegame`` (:class:`SaveGame` or None): The loaded save file, or
           ``None`` if the operation failed.
     :rtype: tuple[bool, str, SaveGame | None]

     :raises OSError:
         If the save file cannot be opened or accessed.

     :seealso:
         - :class:`SaveGame` for the structure of the full save.
         - :func:`load_dict_from_txt` for loading the stored hash.
         - :func:`get_hash` for hash calculation.
         - ``pickle`` for serialization and deserialization behavior.
     """
    if check_hash:
        load_hash = load_dict_from_txt(file_path=filepath_hash)
        if not get_hash(file_name=filepath_hash) == load_hash["hash"]:
            return False, " Corrupted file.", None

    try:
        with open(filepath, "rb") as f:
            savegame = pickle.load(f)
    except:
        return False, "Savegame file have been not found.", None

    return True, f" Welcome back {savegame.player.name}.", savegame


def save_game(player: Player,
              mapgame: Map,
              timeinit: datetime,
              filepath: str = "./save/cfg_save.pkl",
              filepath_hash: str = "./save/cfg_hash.txt"):
    """
    Save the complete game state to disk, including both the ``Player`` and
    ``Map`` instances. The function also updates the player's accumulated
    play time, ensures that all required directories exist, serializes the
    full game state using ``pickle``, and writes a hash file for integrity
    checking.

    Directory paths for ``filepath`` and ``filepath_hash`` are created
    automatically if they do not already exist.

    :param player:
        The ``Player`` instance representing the current game state.
        The player's play time will be refreshed before serialization.
    :type player: Player

    :param mapgame:
        The ``Map`` instance containing world, region, and environmental
        state that must be preserved in the save file.
    :type mapgame: Map

    :param timeinit:
        The datetime representing when the current gameplay session began.
        It is used to compute the additional time played.
    :type timeinit: datetime

    :param filepath:
        The file path where the full serialized save file (``SaveGame``)
        will be written. All intermediate directories will be created
        automatically.
    :type filepath: str

    :param filepath_hash:
        The file path where the hash or integrity metadata will be written.
        All intermediate directories will be created automatically.
    :type filepath_hash: str

    :raises OSError:
        If the function is unable to create directories or write to disk.

    :seealso:
        - :class:`SaveGame` for the full save container.
        - :func:`export_dict_to_txt` for writing auxiliary metadata.
        - ``pickle`` for serialization behavior.
    """
    player.refresh_time_played(time_close=datetime.now(), time_init=timeinit)

    save_dir = os.path.dirname(filepath)
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)

    hash_dir = os.path.dirname(filepath_hash)
    if hash_dir:
        os.makedirs(hash_dir, exist_ok=True)

    save_obj = SaveGame(player=player, mapgame=mapgame)

    with open(filepath, "wb") as f:
        pickle.dump(save_obj, f)

    export_dict_to_txt(dictionary={"hash": get_hash(filepath)}, file_path=filepath_hash)
