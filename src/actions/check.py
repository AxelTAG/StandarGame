# Imports.
# Local imports.
from ..map import Map
from ..player import Player


def check(mapgame: Map,
          player: Player = None,
          target: str = None,
          inventory: bool = False) -> str:
    if player is None:
        return "What do you want to check? CHECK ITEM for items at places or CHECK INV ITEM for items in the inventory."

    if not target or target is None:
        return "What do you want to check? CHECK ITEM for items at places or CHECK INV ITEM for items in the inventory."

    if inventory:
        item_object = player.get_item(item=target)
        if item_object is None:
            "You haven't this item."
        return item_object.description

    if target in player.place.get_items():
        return mapgame.get_item_object(item_id=target).description

    mob = player.place.get_mob(mob_id=target)
    if mob is not None:
        return mob.description

    tree = player.place.get_tree_respawned(tree_id=target)
    if tree is not None:
        return tree.description

    return f"There is no {item.title()} here."
