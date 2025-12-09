# Local imports.
from .actions import buy, sell, get_item, transport
from .. import displays
from .. import utils
from ..enums import NpcTypes, ObjectiveType, QuestStatus
from ..map import Map
from ..npc import Npc
from ..player import Player
from ..quest import Quest
from ..world import ITEMS


def verify_quests_memory(quest1: Quest, quest2: Quest) -> bool:
    if quest1 is quest2:
        return True
    raise Exception


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


def loop_buy(player: Player, npc: Npc, mapgame: Map, craft: bool = False) -> tuple[str, bool]:
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
                                      mapgame=mapgame,
                                      item=items_list[item_index],
                                      quantity=quantity,
                                      cost=prices_list[item_index])
            return transaction, status
    return "", False


def loop_sell(player: Player, npc: Npc, mapgame: Map) -> tuple[str, bool]:
    # Print of items.
    items = get_sell_prices(items=list(player.inventory.items.keys()))
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
                                  mapgame=mapgame,
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


def loop_transport(player: Player, npc: Npc, mapgame: Map):
    # Print of items.
    places = npc.get_transport_places()
    places_without_player_place = {k: v for k, v in places.items() if k != player.place.coordinates}
    places_names = [mapgame.get_biome_name(x=x, y=y) for x, y in places_without_player_place.keys()]
    dict_places = dict(zip(places_names, places_without_player_place.values()))
    places_list, prices_list = displays.disp_show_list_items(player=player, items=dict_places)

    # Place selection.
    number_of_items = len(places_list)
    place_index = get_number(floor_n=1, ceil_n=number_of_items + 1) - 1

    if not place_index == number_of_items:
        if npc.transport_confirm_message is not None:
            displays.disp_standard_tw(npc.name, npc.transport_confirm_message)
        confirmation = get_answer(answers={1: "Yes"})
        if confirmation == 1:
            return transport(player=player,
                             mapgame=mapgame,
                             place=list(places_without_player_place.keys())[place_index],
                             cost=dict_places[places_list[place_index]])
        if npc.transport_arrive_message is not None:
            displays.disp_standard_tw(npc.name, npc.transport_arrive_message)
    return "", False


def talk(npc: Npc,
         player: Player,
         mapgame: Map) -> str:
    # Npc with quest.
    if npc.has_quest():
        quest = npc.get_first_quest()

        if not quest.is_started():
            displays.disp_standard_tw(name=npc.name, message=quest.messages_start[0])  # Printing first message.
            if quest.answers_start:
                answer = get_answer(answers=quest.answers_start)
                if answer == 1:
                    if quest.messages_start.get(1, False):
                        displays.disp_standard_tw(name=npc.name, message=quest.messages_start[answer])
                if answer == 2:
                    return f"You talked with {npc.name.title()}."
            player.add_quest(quest=npc.give_quest(quest=quest))
            verify_quests_memory(quest1=quest, quest2=player.quests_in_progress[-1])
            for item, amount in quest.give_items().items():
                player.add_item(item=item, quantity=amount)
            return f"New quest: {quest.description} You talked with {npc.name.title()}."

        if quest.is_in_progress():
            displays.disp_standard_tw(name=npc.name, message=quest.messages_in_progress[0])
            if quest.answers_in_progress:
                answer = get_answer(answers=quest.answers_start)
                displays.disp_standard_tw(name=npc.name, message=quest.messages_in_progress[answer])
            return f"You talked with {npc.name.title()}."

        if quest.is_completed():
            displays.disp_standard_tw(name=npc.name, message=quest.messages_reward[0])
            if quest.answers_reward:
                answer = get_answer(answers=quest.answers_start)
                if answer == 1:
                    displays.disp_standard_tw(name=npc.name, message=quest.messages_reward[answer])
                if answer == 2:
                    return f"You talked with {npc.name.title()}."
            reward = npc.complete_quest(quest=quest)
            reward_msg = f"{npc.name.title()} gives you: "
            for item, amount in reward.items():
                if item in player.reputation.keys():
                    player.add_reputation(city=item, amount=amount)
                    continue
                player.add_item(item=item, quantity=amount)
                item_object = get_item(item_name=item)
                reward_msg += f"{amount} {item_object.name}, "
            if quest.remove:
                for objetive in filter(lambda q: q.type == ObjectiveType.COLLECT, quest.objectives):
                    player.inventory.discard_item(item=objetive.target, quantity=objetive.amount)
            player.remove_quest(quest=quest)
            return f"{reward_msg[:-2]}. You talked with {npc.name.title()}."
        return f"You talked with {npc.name.title()}."

    # Update of quests with TALK objective.
    player.update_quests(target=npc.id, amount=1)
    # Update of quests with DELIVERY objective.
    for quest in player.get_quests(completed=False):
        for objetive in quest.objectives:
            if objetive.type == ObjectiveType.DELIVER:
                if player.has(item=objetive.deliver_item, amount=objetive.deliver_amount):
                    player.update_quests(target=npc.id,
                                         amount=1,
                                         deliver_item=objetive.deliver_item,
                                         deliver_amount=objetive.deliver_amount)
                    if objetive.is_done():
                        player.inventory.discard_item(item=objetive.deliver_item,
                                                      quantity=objetive.deliver_amount)

    # Npc whithout quests.
    # First message of npc.
    displays.disp_standard_tw(npc.name, npc.messages[0])  # Printing first message.
    npc.hist_messages[0] = True  # Turning True first message of NPC.

    # Npc with skips.
    if npc.npc_type == NpcTypes.CAPTAIN or npc.npc_type == NpcTypes.TRANSPORTER:
        if mapgame.current_time_of_day not in npc.transport_time_of_day:
            return f"You talked with {npc.name.title()}."

    # Npc with answers.
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
                    result, _ = loop_buy(player=player, npc=npc, mapgame=mapgame, craft=False)
                if answer == 2:
                    result, _ = loop_sell(player=player, npc=npc, mapgame=mapgame)

            if npc.npc_type == NpcTypes.TAVERN_KEEPER:
                if answer == 1:
                    result, _ = loop_buy(player=player, npc=npc, mapgame=mapgame, craft=False)
                if answer == 2:
                    result, _ = loop_sell(player=player, npc=npc, mapgame=mapgame)

            if npc.npc_type == NpcTypes.ARTISAN:
                if answer == 1:
                    result, _ = loop_buy(player=player, npc=npc, mapgame=mapgame, craft=True)
                if answer == 2:
                    result, _ = loop_sell(player=player, npc=npc, mapgame=mapgame)

            if npc.npc_type == NpcTypes.INNKEEPER:
                if answer == 1:
                    result, _ = loop_rent(player=player, npc=npc, mapgame=mapgame)
                if answer == 2:
                    result, _ = loop_buy(player=player, npc=npc, mapgame=mapgame, craft=False)

            if npc.npc_type == NpcTypes.CAPTAIN or npc.npc_type == NpcTypes.TRANSPORTER:
                if answer == 1:
                    result, state = loop_transport(player=player, npc=npc, mapgame=mapgame)
                    if state:
                        return result
                    return result

            # Adding result to transactions.
            if result:
                transactions += result

        if npc.name == "whispers":
            return "You heard some whispers. "

    return f"You talked with {npc.name.title()}."  # Break if the npc has no second message.
