# Imports.
# Local imports.
from ..displays import disp_quests
from ..player import Player
from ..map import Map


def quests(player: Player, mapgame: Map, quest_id: str = None) -> str:
    if quest_id is not None:
        if quest_id not in [q.id for q in player.get_quests(completed=False)]:
            return f"You have no {quest_id} quest."
    return disp_quests(player=player, mapgame=mapgame, quest_id=quest_id)
