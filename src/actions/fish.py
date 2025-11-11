# Imports.
# Internal imports.
from ..map import Map
from ..player import Player

# External imports.
import random


def fish(player: Player, mapgame: Map, pace_factor: float = 0.3) -> str:
    fishignpoles = [item for item in player.inventory.get_item_objects if item.fishing]

    if not fishignpoles:
        return "You need a fishingpole to fish."

    if not player.place.get_water(month=mapgame.current_month):
        return "You cannot fish here."

    hours = int(player.place.get_pace(month=mapgame.current_month) * pace_factor)
    mapgame.add_hours(hours_to_add=hours)

    if not player.place.get_fishs_respawned():
        return "You have't caught anything."

    for fish_entitie in player.place.get_fishs_respawned():
        if any([fish_entitie.depth == fishingpole.depth_range for fishingpole in fishignpoles]):
            if fish_entitie.catch_chance >= random.random():
                player.place.remove_respawned_fish(fish=fish_entitie)
                player.add_item(item=fish_entitie.get_drop_item(), quantity=1)
                return f"You have caught a {fish_entitie.name}."
    
    mapgame.add_hours(hours_to_add=hours)
    return "You haven't caught anything."
