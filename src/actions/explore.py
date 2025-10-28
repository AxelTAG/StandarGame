# Imports.
# Local imports.
from ..biome import Biome, Entry
from ..enums import EntryType
from ..map import Map
from ..player import Player

# External imports.
import random


def explore(player: Player,
            mapgame: Map,
            pace_factor: float = 0.5) -> str:
    month = mapgame.current_month

    if player.place.entries is None:
        mapgame.add_hours(hours_to_add=int(player.place.get_pace(month=month) * pace_factor))
        return "You explore the zone but you found nothing."

    if isinstance(player.place, Entry):
        if player.place.entry_type not in [EntryType.CAVE]:
            return "You can't explore here."

    for entrie_id, entrie in player.place.entries.items():
        if type(entrie) == Biome:
            continue

        if entrie.hide is None:
            continue

        if entrie.hide["visibility"]:
            continue

        if entrie.hide["finding_chance"] >= random.random():
            entrie.hide["visibility"] = True
            mapgame.add_hours(hours_to_add=int(player.place.get_pace(month=month) * pace_factor))
            return f"You have found a {entrie.get_name(month=month)}."

        mapgame.add_hours(hours_to_add=int(player.place.get_pace(month=month) * pace_factor))
        return "You explore the zone but you found nothing."

    mapgame.add_hours(hours_to_add=int(player.place.get_pace(month=month) * pace_factor))
    return f"You explore the zone but you found nothing."
