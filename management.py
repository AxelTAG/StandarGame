# Imports.
# Local imports.
from actions import battle, talk
from displays import disp_talk_tw
from enums import NpcTypes, TimeOfDay
from globals import ENTRIES, MOBS
from map import Map
from player import Player
from utils import export_dict_to_txt, get_hash, export_player

# External imports.
from datetime import datetime


# Event handler.
def event_handler(player: Player,
                  map_game: Map,
                  time_init: datetime) -> tuple[int, int]:
    # Event of Goblin Chief (1/3).
    if player.place == ENTRIES["sub_cave_2_2"] and not player.events["goblin_chief_crown_1"]:
        talk(npc=map_game.npcs["goblin griznuk"], player=player, map_game=map_game)

        play, menu, win = battle(player=player, enemy=MOBS["goblin chief"], map_game=map_game)

        if win:
            talk(npc=map_game.npcs["mayors daughter maisie"], player=player, map_game=map_game)

            map_game.npcs["mayors daughter maisie"].messages = {
                0: ["My father, the mayor, will want to thank you properly. Please, come back with me to the village.",
                    "Words cannot express my gratitude, but I hope our people can repay  your bravery."]}

            player.events["goblin_chief_crown_1"] = True

        return play, menu

    # Event of Goblin Chief (2/3).
    if ((player.last_place == map_game.map_settings[(9, 4)] or player.last_place == map_game.map_settings[(10, 5)])
            and player.events["goblin_chief_crown_1"]
            and not player.events["goblin_chief_crown_2"]):
        map_game.npcs["mayor thorian"].reset_hist_messages()

        map_game.npcs["mayors daughter maisie"].messages = {
            0: ["Thank you, brave one!",
                "If not for your help, I might have tried to escape through one of the hidden passages in the cave.",
                "I saw them but had no chance to explore. Your courage saved me before I could take the risk.",
                "I owe you my life."]}
        map_game.npcs["mayors daughter maisie"].place = [(10, 4)]
        map_game.npcs["mayors daughter maisie"].place_morning = [(10, 4)]
        map_game.npcs["mayors daughter maisie"].place_evening = [(10, 4), "house_epiiat_mayor"]

        map_game.npcs["mayor thorian"].messages = {
            0: ["I’ve heard the tale from my daughter, Maisie. You rescued her from the clutches of those "
                "vile goblins.",
                "I thank you, not as a mayor, but as a father. Our village owes you a debt we cannot repay.",
                "Please, accept this reward—a small token of our gratitude. Epiiat's doors are always open to you,"
                " brave soul."]}
        map_game.npcs["villager merrin"].messages = {
            0: ["You did it! You brought Maisie back safely. I can’t thank you enough.",
                "The whole village has been in distress since she went missing. You’ve given us hope again, brave one.",
                "We’ll not forget what you’ve done for Epiiat."]}
        map_game.npcs["villager fira"].messages = {
            0: ["I just heard the news—Maisie is safe and back home. What a blessing for the whole village.",
                "We’ve all been on edge since she went missing. It feels like a dark cloud has finally "
                "lifted from Epiiat."]}

        player.inventory.add_item(item="hardened_leather_armor", quantity=1)
        player.events["goblin_chief_crown_2"] = True

    # Event of Goblin Chief (3/3).
    if (player.events["goblin_chief_crown_2"] and map_game.npcs["mayor thorian"].hist_messages[0]
            and not player.events["goblin_chief_crown_3"]):
        map_game.npcs["mayor thorian"].messages = {
            0: ["It’s rare to find such selfless bravery in these dark times. Thanks to you, my daughter is "
                "safe, and Epiiat breathes easier tonight.",
                "I must ensure the village knows of this deed; tales of courage like this must be remembered.",
                "May the gods guide that your steps, wherever the road may lead."]}

        player.events["goblin_chief_crown_3"] = True

    # Event Fisherman Marlin quests (1/9).
    if not player.events["marlin_quests_1"] and map_game.npcs["fisherman marlin"].hist_messages[1]:
        player.inventory.add_item(item="marlins_fish_tuna", quantity=2)

        map_game.npcs["fisherman marlin"].reset_hist_messages()
        map_game.npcs["fisherman brann"].reset_hist_messages()

        map_game.npcs["fisherman marlin"].messages = {
            0: ["Ah, it’s you! Tell me, have you managed to deliver that fish to my friend in the south? I’ve been "
                "wondering if it arrived fresh!"]}

        map_game.npcs["fisherman marlin"].answers = {}

        map_game.npcs["fisherman brann"].messages = {
            0: ["Oh, by the tides! You’ve brought Marlin’s tuna, haven’t you? I wasn’t sure he’d manage to send it.",
                "Thank you, traveler! This means more to me than you know."]}

        player.events["marlin_quests_1"] = True

    # Event Fisherman Marlin quests (2/9).
    if all([player.events["marlin_quests_1"],
            not player.events["marlin_quests_2"],
            map_game.npcs["fisherman brann"].hist_messages[0]]):
        player.inventory.drop_item(item="marlins_fish_tuna", quantity=2)

        map_game.npcs["fisherman marlin"].reset_hist_messages()

        map_game.npcs["fisherman brann"].messages = {
            0: ["Ah, traveler! Good to see you again.",
                "Thanks to you, Marlin’s tuna was a real treat. How’s the road treating you?"]}

        map_game.npcs["fisherman marlin"].messages = {
            0: ["Thank you for delivering the tuna to Brann! You’ve been a great help.",
                "But now I’m worried about another shipment I sent with a caravan to Epiiat.",
                "I haven’t heard back from them. Could you check on it for me? I’d be truly grateful."]}

        map_game.npcs["caravan leader darek"].place = [(16, 5)]
        map_game.npcs["caravenner lorien"].place = [(16, 5)]
        map_game.npcs["jester ralzo"].place = [(16, 5)]
        map_game.npcs["traveler kaelen"].place = [(16, 5)]

        player.events["marlin_quests_2"] = True

    # Event Fisherman Marlin quests (3/9).
    if all([player.events["marlin_quests_2"],
            not player.events["marlin_quests_3"],
            map_game.npcs["fisherman marlin"].hist_messages[0]]):

        map_game.npcs["fisherman marlin"].messages = {
            0: ["Thanks again for delivering that order to Brann! Now, there’s something else...",
                "I’m worried about a shipment I sent with a caravan to Epiiat. I haven’t heard from them.",
                "Could you check on them for me? I’d really appreciate it."]}

    # Event Fisherman Marlin quests (4/9).
    if all([player.events["marlin_quests_2"],
            not player.events["marlin_quests_3"],
            map_game.npcs["fisherman marlin"].hist_messages[0],
            map_game.npcs["caravan leader darek"].hist_messages[0]]):
        map_game.npcs["fisherman marlin"].reset_hist_messages()

        map_game.npcs["fisherman marlin"].messages = {
            0: ["A derrumbe in the valley? That explains the delay. Thank you for letting me know!",
                "If you're willing, could you deliver them some explosives to clear the way?",
                "I think I saw Captain Thorne loading some onto his ship recently. He might be able to help."]}

        player.events["marlin_quests_3"] = True

    # Event Fisherman Marlin quests (5/9).
    if all(["rocks" not in map_game.map_settings[(15, 5)].req,
            player.events["marlin_quests_3"],
            not player.events["marlin_quests_4"]]):
        map_game.npcs["fisherman marlin"].reset_hist_messages()

        map_game.npcs["fisherman marlin"].messages = {
            0: ["Ah, you've done it! The valley is clear at last. I can’t thank you enough for your help.",
                "Here, take this as a token of my gratitude.",
                "But before you go, I have one last favor to ask. Could you deliver this package to Antina for me?",
                "Take these 3 tunas to a villager named Gareth. The guards won’t trouble you; this permit will grant "
                "you passage.",
                "Safe travels, my friend. Antina awaits!"]}

        map_game.npcs["caravan leader darek"].messages = {
            0: ["You’ve done us a great service, adventurer! Thanks to you, the road is clear, and we can finally "
                "make our way to Epiiat. Safe travels, friend!"]}

        map_game.npcs["caravenner lorien"].messages = {
            0: ["At last, I’ll see Epiiat again! Thank you, traveler. It’s been too long since I walked its streets."]}

        map_game.npcs["jester ralzo"].messages = {
            0: ["Oh, glorious news! Back to Epiiat I go, ready to dazzle with my finest show! Care to attend,"
                " traveler?"]}

        map_game.npcs["traveler kaelen"].messages = {
            0: ["Well done, traveler! You’ve handled that kegpowder with real skill. Not everyone could pull that off.",
                "The road's better thanks to you!"]}

        map_game.map_settings[(14, 5)].description = ("Desolate, silent valley, cracked earth stretches between "
                                                      "imposing cliffs, where an eerie stillness envelops the barren "
                                                      "landscape, untouched by the whispers of wind or the rustle"
                                                      " of life.")

        player.events["caravan_date_arrive"] = map_game.estimate_date(days=3)
        player.events["marlin_quests_4"] = True

    # Event Fisherman Marlin quests (6/9).
    if all([player.events["marlin_quests_4"],
            not player.events["caravan_arrive"]]):
        if map_game.is_major_date(first_date=player.events["caravan_date_arrive"], second_date=map_game.current_date):
            map_game.npcs["caravan leader darek"].messages_morning = {
                0: ["Safe and sound in Epiiat, thanks to you. The goods are delivered, and the road is clear. Well "
                    "done, traveler."]}
            map_game.npcs["caravan leader darek"].messages_evening = {
                0: ["Night falls heavy in this cavern, but at least we're safe for now. You've earned a rest,"
                    " traveler."]}
            map_game.npcs["caravan leader darek"].place_morning = [(9, 5)]
            map_game.npcs["caravan leader darek"].place_evening = [(9, 5), "inn", "main_room"]

            map_game.npcs["caravenner lorien"].messages_morning = {
                0: ["Ah, Epiiat... It's been too long. Feels good to be back. Thanks for making it happen, friend."]}
            map_game.npcs["caravenner lorien"].messages_evening = {
                0: ["Heh... y'know, every time I come to Epiiat, I feel... happy. It’s ‘cause of the mayor’s"
                    " daughter.",
                    "She’s... she’s wonderful. Don’t tell anyone, alright?"]}
            map_game.npcs["caravenner lorien"].place_morning = [(9, 4)]
            map_game.npcs["caravenner lorien"].place_evening = [(9, 5), "inn"]

            map_game.npcs["jester ralzo"].messages_morning = {
                0: ["Epiiat welcomes me once more! Time to lift spirits and stir laughter. Don’t miss my next act, "
                    "hero!"]}
            map_game.npcs["jester ralzo"].messages_night = {
                0: ["A cavern’s as good a stage as any! Care to join us, hero? Music brightens even the darkest"
                    " corners!"]}
            map_game.npcs["jester ralzo"].place_morning = [(9, 5)]
            map_game.npcs["jester ralzo"].place_night = [(9, 5), "inn"]

            player.events["caravan_arrive"] = True

    # Event Fisherman Marlin quests (7/9).
    if all([player.events["marlin_quests_4"],
            not player.events["marlin_quests_5"],
            map_game.npcs["fisherman marlin"].hist_messages[0]]):
        map_game.npcs["fisherman marlin"].reset_hist_messages()

        player.inventory.add_item(item="fishing_pole", quantity=1)
        player.inventory.add_item(item="marlins_fish_tuna", quantity=3)

        map_game.npcs["fisherman marlin"].messages = {
            0: ["Ah, have you managed to deliver those tunas to Gareth yet?",
                "I hope he’s gotten them by now. He's been waiting on those for quite some time. Let me know if you"
                "ran into any trouble!"]}

        player.events["marlin_quests_5"] = True
        player.events["antinas_permission"] = True

    # Event Fisherman Marlin quests (8/9).
    if all([player.events["marlin_quests_5"],
            not player.events["marlin_quests_6"],
            map_game.npcs["villager gareth"].hist_messages[0]]):
        map_game.npcs["fisherman marlin"].reset_hist_messages()

        map_game.npcs["villager gareth"].messages = {
            0: ["Ah, it’s you again! Always good to see a friendly face around here. How's the journey treating "
                "you? Hopefully, the sea's been kinder today!"]}

        map_game.npcs["fisherman marlin"].messages = {
            0: ["Ah, you’ve delivered the tunas to Gareth! Thank you so much for handling that.",
                "He’s a good friend of mine, and I’m glad you could help. I owe you one, adventurer.",
                "If you ever need something from me, you know where to find me!"]}

        player.events["marlin_quests_6"] = True

        # Event Fisherman Marlin quests (9/9).
    if all([player.events["marlin_quests_6"],
            map_game.npcs["fisherman marlin"].hist_messages[0]]):

        map_game.npcs["fisherman marlin"].messages_morning = {
            0: ["Ah, it's a quiet day today. The sea's calm, but the fish are being stubborn.",
                "Still, there's always something peaceful about being near the water.",
                "If you’re ever in need of some good fish, you know where to find me."]}

    # Event batle with Dragon FireFrost after winning.
    if map_game.npcs["dragon firefrost"].hist_messages[0]:
        play, menu, win = battle(player=player, enemy=MOBS["dragon"].copy(), map_game=map_game)
        if win:
            map_game.npcs["dragon firefrost"].message = [
                "Impressive. Today, the winds of fate favor you.",
                "I yield. But heed my words, for when the stars align in a different cosmic dance, I shall await you"
                " once more.",
                "Until then, let the echoes of our encounter linger in the mountain breeze."
                " Farewell, " + player.name + ".",
                "Until our destinies entwine again."],

            talk(npc=map_game.npcs["dragon firefrost"], player=player, map_game=map_game)

            map_game.map_settings[(11, 24)].description = ("Frozen valley, a pristine, snow-covered expanse where "
                                                           "frost-kissed silence reigns. Glistening ice formations "
                                                           "adorn the landscape, creating an ethereal and serene "
                                                           "winter tableau in nature's icy embrace.")
            map_game.map_settings[(11, 24)].npc = []
            map_game.map_settings[(0, 0)].entries["hut"].items.append("origami_flowers")
            map_game.npcs["dragon firefrost"] = [[], [], [], [0]]

            return play, menu
        else:
            map_game.npcs["dragon firefrost"].reset_hist_messages()
            save(player=player, map_game=map_game, time_init=time_init)
            return play, menu

    return True, False


def map_control_handling(player: Player,
                         map_game: Map):
    # Control of Innkeeper room expirations.
    for npc in player.place.npc:
        if map_game.npcs[npc].npc_type == NpcTypes.INNKEEPER:
            expirated_room_keys = map_game.check_room_expiration(player=player, npc=npc)
            for key in expirated_room_keys:
                player.inventory.drop_item(item=key, quantity=player.inventory.items[key])
                disp_talk_tw(npc=map_game.npcs[npc],
                             message=["Ah, there you are. Your stay was pleasant, I hope. But your days are up, "
                                      "traveler. I’ll need the room key back now. Don’t worry—you’re welcome to rent "
                                      "it again if you plan on staying longer."])

    # Sailor Kael detention.
    if "sailor kael" in player.place.npc and player.place == map_game.map_settings[(27, 15)].entries["thornes_ship"]:
        talk(npc=map_game.npcs["sailor kael"], player=player, map_game=map_game)
        player.set_place(place=player.last_place)

    if "guard lorian" in player.last_place.npc and player.place == map_game.map_settings[(12, 17)]:
        if not player.events["antinas_permission"]:
            talk(npc=map_game.npcs["guard lorian"], player=player, map_game=map_game)
            player.set_place(place=player.last_place)


# Load game function.
def load_game(path_usavepkl: str = "cfg_save.pkl", path_msave: str = "cfg_map.txt",
              path_settingpkl: str = "cfg_setting.pkl", path_hsave: str = "cfg_hash.txt"):
    pass


# Save function.
def save(player: Player,
         map_game: Map,
         time_init: datetime,
         path_usavepkl: str = "cfg_save.pkl",
         path_mappkl: str = "cfg_map.pkl",
         path_hsave: str = "cfg_hash.txt") -> None:
    player.refresh_time_played(datetime.now(), time_init)

    # Inventory, user stats and map setting saving (export to txt).
    export_player(player, path_usavepkl)
    export_player(map_game, path_mappkl)

    # Hash saving (export to dict).
    export_dict_to_txt(dictionary={"hash": get_hash(path_usavepkl)}, file_path=path_hsave)
