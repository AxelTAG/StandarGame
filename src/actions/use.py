# Imports.
# Local imports.
from ..item import Item
from ..player import Player
from ..map import Map


def use(player: Player, mapgame: Map = None, item: str | Item = None) -> tuple[str, bool]:
    if isinstance(item, Item):
        item = item.id

    if item is None:
        return "You cannot use None.", False

    if item == "gold":
        return f"You can't use {item.replace('_', ' ').title()}.", False

    if item not in player.inventory.items.keys():
        return f"You have no {item.replace('_', ' ').title()}.", False

    if player.inventory.items[item] > 0:
        if "potion" in item:
            if item == "giant_red_potion":
                player.heal(amount=40)

            elif item == "red_potion":
                player.heal(amount=25)

            elif item == "little_red_potion":
                player.heal(amount=10)

            else:
                return "Nothing done.", False

            player.inventory.discard_item(item=item, quantity=1)

            return f"{player.name}'s HP refilled to {player.hp}!", True

        elif "antidote" in item:
            player.heal_poisoning()
            player.inventory.discard_item(item=item, quantity=1)

            return "You have taken the antidote.", True

        elif "powder_keg" in item:
            explosion = False
            for neighbor in mapgame.neighbors_from_coord((player.x, player.y)):
                if "rocks" in neighbor.req:
                    neighbor.req.remove("rocks")
                    player.inventory.discard_item(item=item, quantity=1)
                    explosion = True
            if explosion:
                return "You have explode the keg powder on all the rocks.", True
            else:
                return "There is nothing to explode here.", False

        else:
            return "You can't use this item.", False
    else:
        return f"You have no more {item.replace('_', ' ').title()}.", False
