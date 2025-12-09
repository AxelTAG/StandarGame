# Imports.
# Local imports.
from ..enums import StatType
from ..item import Item
from ..player import Player
from ..map import Map
from ..world import BUFFS


def use(player: Player,
        mapgame: Map = None,
        item: str | Item = None) -> tuple[str, bool]:
    if isinstance(item, str):
        item = player.inventory.get_item_object(item=item)

    if item is None:
        return "You cannot use this.", False

    if item.id == "gold":
        return f"You can't use {item.name.title()}.", False

    if not player.has(item=item.id, amount=1):
        return f"You have no {item.name.title()}.", False

    # Potions.
    if item.id == "little_red_potion":
        player.heal(amount=10)
        player.inventory.discard_item(item=item.id, quantity=1)
        return f"{player.name}'s HP refilled to {player.hp}!", True

    if item.id == "red_potion":
        player.heal(amount=25)
        player.inventory.discard_item(item=item.id, quantity=1)
        return f"{player.name}'s HP refilled to {player.hp}!", True

    if item.id == "giant_red_potion":
        player.heal(amount=40)
        player.inventory.discard_item(item=item.id, quantity=1)
        return f"{player.name}'s HP refilled to {player.hp}!", True

    if item.id == "antidote":
        player.heal_poisoning(amount=3)
        player.inventory.discard_item(item=item.id, quantity=1)
        return "You have taken the antidote.", True

    if item.id == "little_strength_potion":
        player.add_buff(buff=BUFFS[item.id])
        player.inventory.discard_item(item=item.id, quantity=1)
        return "You feel a small surge of strength.", True

    # Others.
    if item.id == "powder_keg":
        explosion = False
        for neighbor in mapgame.neighbors_from_coord((player.x, player.y)):
            if "rocks" in neighbor.req:
                neighbor.req.remove("rocks")
                neighbor.remove_item("rocks", player=player)
                player.inventory.discard_item(item=item.id, quantity=1)
                explosion = True
        if explosion:
            return "You have explode the keg powder on all the rocks.", True
        return "There is nothing to explode here.", False
    return "You can't use this item.", False
