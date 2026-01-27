# Import.
# Local imports.
from ..management.save import load_game
from ..map import Map
from ..player import Player


def catch_dream(filepath: str, player: Player, mapgame: Map) -> str:
    # Getting old instances.
    load_state, _, savegame = load_game(filepath=filepath, check_hash=False)

    if not load_state:
        return "Dream was not catched."

    old_mapgame = savegame.mapgame
    old_player = savegame.player

    # Update of map.
    mapgame.update_from_instance(old=old_mapgame)

    # Update of player.
    player.update_from_instance(old=old_player, mapgame=mapgame)

    # Excutios of events.
    # for event in mapgame.events:
    #     if event.was_executed:
    #         event.action(player=player, mapgame=mapgame, update=True)

    return "Dream was catched."
