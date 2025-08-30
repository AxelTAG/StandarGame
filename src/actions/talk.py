# Local imports.
import displays
import utils
from actions.actions import buy, sell, get_item
from enums import NpcTypes
from map import Map
from npc import Npc
from player import Player
from world import ITEMS


def get_number(floor_n: int = 0, ceil_n: int = 10) -> int | None:
    while True:
        try:
            number = int(input(displays.INPUT_LABEL))
            if floor_n <= number <= ceil_n:
                return number
        except ValueError:  # Bucle will reset if input is not an intenger.
            pass


def get_answer(answers: dict) -> int | None:
    while True:
        if answers.keys():
            displays.disp_talk_answers(answers=answers)  # Printing answers.
            number_answers = len(answers)

            return get_number(floor_n=1, ceil_n=number_answers + 1)


def get_sell_prices(items: list[str]) -> dict:
    item_names, sell_prices = [], []
    for item in items:
        item_object = get_item(item_name=item)
        sell_prices.append({"gold": item_object.sell_price})
    return dict(zip(items, sell_prices))


def loop_buy(player: Player, npc: Npc, craft: bool = False) -> tuple[str, bool]:
    # Print of items.
    items = npc.get_trading_items(item_base=ITEMS)
    items_list, prices_list = displays.disp_show_list_items(player=player, items=items)

    # Item selection.
    number_of_items = len(items_list)
    item_index = get_number(floor_n=1, ceil_n=number_of_items + 1) - 1

    # Quantity selection.
    if not item_index == number_of_items:  # Quit condition.
        item_name = utils.underscores(items_list[item_index])

        print(f"{' ' * 4}{npc.get_quantity_message(item=item_name, buy=not craft, craft=craft)}")

        quantity = get_number(floor_n=0, ceil_n=999)
        if not quantity == 0:
            transaction, status = buy(player=player,
                                      item=items_list[item_index],
                                      quantity=quantity,
                                      cost=prices_list[item_index])
            return transaction, status
    return "", False


def loop_sell(player: Player, npc: Npc) -> tuple[str, bool]:
    # Print of items.
    items = get_sell_prices(items=player.inventory.items.keys())
    items_list, prices_list = displays.disp_show_list_items(player=player, items=items, player_quantity=True)

    # Item selection.
    number_of_items = len(items_list)
    item_index = get_number(floor_n=1, ceil_n=number_of_items + 1) - 1

    # Quantity selection.
    if not item_index == number_of_items:  # Quit condition.
        item_name = utils.underscores(items_list[item_index]).title()

        print(f"{' ' * 4}{npc.get_quantity_message(item=item_name, sell=True)}")

        quantity = get_number(floor_n=0,
                              ceil_n=999)
        if not quantity == 0:
            transaction, status = sell(player=player,
                                       item=items_list[item_index],
                                       quantity=quantity,
                                       price=prices_list[item_index]["gold"])
            return transaction, status
    return "", False


def loop_rent(player: Player, npc: Npc, mapgame: Map) -> tuple[str, bool]:
    # Print of items.
    items = npc.get_bed_items()
    items_list, prices_list = displays.disp_show_list_items(player=player, items=items)

    # Item selection.
    number_of_items = len(items_list)
    item_index = get_number(floor_n=1, ceil_n=number_of_items + 1) - 1

    if not item_index == number_of_items:  # Quit condition.
        transaction, status = buy(player=player,
                                  item=items_list[item_index],
                                  quantity=1,
                                  cost=prices_list[item_index])
        if status:
            displays.disp_standard_tw(name=npc.name, message=[npc.bed_key_message])
            expiration_date = ITEMS[items_list[item_index]].expiration
            npc.room_expirations[items_list[item_index]] = mapgame.estimate_date(days=expiration_date)
            return transaction, status

        displays.disp_standard_tw(name=npc.name, message=[npc.bed_low_message])
        return transaction, status
    return "", False


def talk(npc: Npc,
         player: Player,
         mapgame: Map) -> str:
    # # Npc with quest.
    # if npc.has_quest():
    #     quest = npc.get_first_quest()
    #
    #     if not quest.is_started():
    #         displays.disp_standard_tw(npc.name, quest.messages_npc[0])  # Printing first message.
    #         quest.start()
    #         return f"You talked with {npc.name.title()}."

    # First message of npc.
    displays.disp_standard_tw(npc.name, npc.messages[0])  # Printing first message.
    npc.hist_messages[0] = True  # Turning True first message of NPC.

    transactions, result = "", ""
    while bool(npc.answers.keys()):
        # Answers for npc.
        if npc.answers.keys():
            answer = get_answer(answers=npc.answers)
            leave_condition = len(npc.answers) + 1

            if answer == leave_condition:  # Exit talk action.
                if npc.leave_message:
                    displays.disp_standard_tw(npc.name, npc.leave_message)  # Printing leave message.
                if transactions:
                    return transactions + f" You talked with {npc.name.title()}."  # Returning transactions.
                return f"You talked with {npc.name.title()}."

            # Second message of npc.
            displays.disp_standard_tw(npc.name, npc.messages[answer])
            npc.hist_messages[answer] = True  # Turning True message of NPC.

            if npc.npc_type == NpcTypes.MERCHANT:
                if answer == 1:
                    result, _ = loop_buy(player=player, npc=npc, craft=False)
                if answer == 2:
                    result, _ = loop_sell(player=player, npc=npc)

            if npc.npc_type == NpcTypes.TAVERN_KEEPER:
                if answer == 1:
                    result, _ = loop_buy(player=player, npc=npc, craft=False)
                if answer == 2:
                    result, _ = loop_sell(player=player, npc=npc)

            if npc.npc_type == NpcTypes.ARTISAN:
                if answer == 1:
                    result, _ = loop_buy(player=player, npc=npc, craft=True)
                if answer == 2:
                    result, _ = loop_sell(player=player, npc=npc)

            if npc.npc_type == NpcTypes.INNKEEPER:
                if answer == 1:
                    result, _ = loop_rent(player=player, npc=npc, mapgame=mapgame)

                if answer == 2:
                    result, _ = loop_buy(player=player, npc=npc, craft=False)

            # Adding result to transactions.
            if result:
                transactions += result

        if npc.name == "whispers":
            return "You heard some whispers. "

    return f"You talked with {npc.name.title()}."  # Break if the npc has no second message.
