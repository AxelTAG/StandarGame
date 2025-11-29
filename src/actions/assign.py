# Imports.
# Local imports.
from ..player import Player


def assign(player: Player, stat: str, quantity: int = 1) -> str:
    if quantity > player.st_points:
        return f"You don't have enough skill points [{player.st_points}]."
    if player.st_points == 0:
        return "You have no more skill points left."

    if player.st_points:
        if stat in ["strength", "str"]:
            player.strength += quantity
            player.st_points -= quantity
            return "You have assigned {quantity} skill point to strength."
        elif stat in ["agility", "agi"]:
            player.agility += quantity
            player.st_points -= quantity
            return f"You have assigned {quantity} skill point to agility."
        elif stat in ["resistance", "res"]:
            player.resistance += quantity
            player.st_points -= quantity
            return f"You have assigned {quantity} skill point to resistance."
        elif stat in ["vitality", "vit"]:
            player.vitality += quantity
            player.st_points -= quantity
            return f"You have assigned {quantity} skill point to vitality."
    return "That is not posible."
