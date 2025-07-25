# Imports.
# Local imports.
import globals
import utils
from actions import battle, talk
from displays import disp_talk_tw
from enums import NpcTypes
from globals import ENTRIES, MOBS
from map import Map
from player import Player

# External imports.
import copy
import pickle
import time
from datetime import datetime


# Event handler.
def event_handler(player: Player,
                  mapgame: Map,
                  time_init: datetime) -> tuple[int, int]:
    # Event of Goblin Chief (1/3).
    goblin_chiefs_bedroom = mapgame.place_from_list([(13, 0), "cave_entrance", "cave_pit", "cave_basin",
                                                     "cave_gallery", "chiefs_cave", "goblin_chief_bedroom"])

    if player.place == goblin_chiefs_bedroom and not player.events["goblin_chief_crown_1"]:
        talk(npc=mapgame.npcs["goblin_griznuk"], player=player, map_game=mapgame)

        play, menu, win = battle(player=player, enemy=copy.deepcopy(MOBS["goblin chief"]), map_game=mapgame)

        if win:
            talk(npc=mapgame.npcs["mayors_daughter_maisie"], player=player, map_game=mapgame)

            mapgame.npcs["mayors_daughter_maisie"].messages = {
                0: ["My father, the mayor, will want to thank you properly. Please, come back with me to the village.",
                    "Words cannot express my gratitude, but I hope our people can repay  your bravery."]}

            player.events["goblin_chief_crown_1"] = True

        return play, menu

    # Event of Goblin Chief (2/3).
    if ((player.last_place == mapgame.map_settings[(9, 4)] or player.last_place == mapgame.map_settings[(10, 5)])
            and player.events["goblin_chief_crown_1"]
            and not player.events["goblin_chief_crown_2"]):
        mapgame.npcs["mayor_thorian"].reset_hist_messages()

        mapgame.npcs["mayors_daughter_maisie"].messages = {
            0: ["Thank you, brave one!",
                "If not for your help, I might have tried to escape through one of the hidden passages in the cave.",
                "I saw them but had no chance to explore. Your courage saved me before I could take the risk.",
                "I owe you my life."]}
        mapgame.npcs["mayors_daughter_maisie"].place = [(10, 4)]
        mapgame.npcs["mayors_daughter_maisie"].place_morning = [(10, 4)]
        mapgame.npcs["mayors_daughter_maisie"].place_evening = [(10, 4), "mayors_house"]

        mapgame.npcs["mayor_thorian"].messages = {
            0: ["I’ve heard the tale from my daughter, Maisie. You rescued her from the clutches of those "
                "vile goblins.",
                "I thank you, not as a mayor, but as a father. Our village owes you a debt we cannot repay.",
                "Please, accept this reward—a small token of our gratitude. Epiiat's doors are always open to you,"
                " brave soul."]}
        mapgame.npcs["villager_merrin"].messages = {
            0: ["You did it! You brought Maisie back safely. I can’t thank you enough.",
                "The whole village has been in distress since she went missing. You’ve given us hope again, brave one.",
                "We’ll not forget what you’ve done for Epiiat."]}
        mapgame.npcs["villager_fira"].messages = {
            0: ["I just heard the news—Maisie is safe and back home. What a blessing for the whole village.",
                "We’ve all been on edge since she went missing. It feels like a dark cloud has finally "
                "lifted from Epiiat."]}

        player.add_item(item="hardened_leather_armor", quantity=1)
        player.events["goblin_chief_crown_2"] = True

    # Event of Goblin Chief (3/3).
    if (player.events["goblin_chief_crown_2"] and mapgame.npcs["mayor_thorian"].hist_messages[0]
            and not player.events["goblin_chief_crown_3"]):
        mapgame.npcs["mayor_thorian"].messages = {
            0: ["It’s rare to find such selfless bravery in these dark times. Thanks to you, my daughter is "
                "safe, and Epiiat breathes easier tonight.",
                "I must ensure the village knows of this deed; tales of courage like this must be remembered.",
                "May the gods guide that your steps, wherever the road may lead."]}

        player.events["goblin_chief_crown_3"] = True

    # Event Fisherman Marlin quests (1/9).
    if not player.events["marlin_quests_1"] and mapgame.npcs["fisherman_marlin"].hist_messages[1]:
        player.add_item(item="marlins_fish_tuna", quantity=2)

        mapgame.npcs["fisherman_marlin"].reset_hist_messages()
        mapgame.npcs["fisherman_brann"].reset_hist_messages()

        mapgame.npcs["fisherman_marlin"].messages = {
            0: ["Ah, it’s you! Tell me, have you managed to deliver that fish to my friend in the south? I’ve been "
                "wondering if it arrived fresh!"]}

        mapgame.npcs["fisherman_marlin"].answers = {}

        mapgame.npcs["fisherman_brann"].messages = {
            0: ["Oh, by the tides! You’ve brought Marlin’s tuna, haven’t you? I wasn’t sure he’d manage to send it.",
                "Thank you, traveler! This means more to me than you know."]}

        player.events["marlin_quests_1"] = True

    # Event Fisherman Marlin quests (2/9).
    if all([player.events["marlin_quests_1"],
            not player.events["marlin_quests_2"],
            mapgame.npcs["fisherman_brann"].hist_messages[0]]):
        player.inventory.drop_item(item="marlins_fish_tuna", quantity=2)

        mapgame.npcs["fisherman_marlin"].reset_hist_messages()

        mapgame.npcs["fisherman_brann"].messages = {
            0: ["Ah, traveler! Good to see you again.",
                "Thanks to you, Marlin’s tuna was a real treat. How’s the road treating you?"]}

        mapgame.npcs["fisherman_marlin"].messages = {
            0: ["Thank you for delivering the tuna to Brann! You’ve been a great help.",
                "But now I’m worried about another shipment I sent with a caravan to Epiiat.",
                "I haven’t heard back from them. Could you check on it for me? I’d be truly grateful."]}

        mapgame.npcs["caravan_leader_darek"].place = [(16, 5)]
        mapgame.npcs["caravenner_lorien"].place = [(16, 5)]
        mapgame.npcs["jester_ralzo"].place = [(16, 5)]
        mapgame.npcs["traveler_kaelen"].place = [(16, 5)]

        player.events["marlin_quests_2"] = True

    # Event Fisherman Marlin quests (3/9).
    if all([player.events["marlin_quests_2"],
            not player.events["marlin_quests_3"],
            mapgame.npcs["fisherman_marlin"].hist_messages[0]]):
        mapgame.npcs["fisherman_marlin"].messages = {
            0: ["Thanks again for delivering that order to Brann! Now, there’s something else...",
                "I’m worried about a shipment I sent with a caravan to Epiiat. I haven’t heard from them.",
                "Could you check on them for me? I’d really appreciate it."]}

    # Event Fisherman Marlin quests (4/9).
    if all([player.events["marlin_quests_2"],
            not player.events["marlin_quests_3"],
            mapgame.npcs["fisherman_marlin"].hist_messages[0],
            mapgame.npcs["caravan_leader_darek"].hist_messages[0]]):
        mapgame.npcs["fisherman_marlin"].reset_hist_messages()

        mapgame.npcs["fisherman_marlin"].messages = {
            0: ["A derrumbe in the valley? That explains the delay. Thank you for letting me know!",
                "If you're willing, could you deliver them some explosives to clear the way?",
                "I think I saw Captain Thorne loading some onto his ship recently. He might be able to help."]}

        player.events["marlin_quests_3"] = True

    # Event Fisherman Marlin quests (5/9).
    if all(["rocks" not in mapgame.map_settings[(15, 5)].req,
            player.events["marlin_quests_3"],
            not player.events["marlin_quests_4"]]):
        mapgame.npcs["fisherman_marlin"].reset_hist_messages()

        mapgame.npcs["fisherman_marlin"].messages = {
            0: ["Ah, you've done it! The valley is clear at last. I can’t thank you enough for your help.",
                "Here, take this as a token of my gratitude.",
                "But before you go, I have one last favor to ask. Could you deliver this package to Antina for me?",
                "Take these 3 tunas to a villager named Gareth. The guards won’t trouble you; this permit will grant "
                "you passage.",
                "Safe travels, my friend. Antina awaits!"]}

        mapgame.npcs["caravan_leader_darek"].messages = {
            0: ["You’ve done us a great service, adventurer! Thanks to you, the road is clear, and we can finally "
                "make our way to Epiiat. Safe travels, friend!"]}

        mapgame.npcs["caravenner_lorien"].messages = {
            0: ["At last, I’ll see Epiiat again! Thank you, traveler. It’s been too long since I walked its streets."]}

        mapgame.npcs["jester_ralzo"].messages = {
            0: ["Oh, glorious news! Back to Epiiat I go, ready to dazzle with my finest show! Care to attend,"
                " traveler?"]}

        mapgame.npcs["traveler_kaelen"].messages = {
            0: ["Well done, traveler! You’ve handled that kegpowder with real skill. Not everyone could pull that off.",
                "The road's better thanks to you!"]}

        mapgame.npcs["worker_gorrick"].messages = {
            0: ["Finally, the valley is cl...",
                "Zzzz... Zzz..."]}
        mapgame.npcs["worker_gorrick"].place = [(10, 4), "wooden_house"]

        mapgame.map_settings[(14, 5)].description = ("Desolate, silent valley, cracked earth stretches between "
                                                     "imposing cliffs, where an eerie stillness envelops the barren "
                                                     "landscape, untouched by the whispers of wind or the rustle"
                                                     " of life.")

        player.events["caravan_date_arrive"] = mapgame.estimate_date(days=3)
        player.events["marlin_quests_4"] = True

    # Event Fisherman Marlin quests (6/9).
    if all([player.events["marlin_quests_4"],
            not player.events["caravan_arrive"]]):
        if mapgame.is_major_date(first_date=player.events["caravan_date_arrive"], second_date=mapgame.current_date):
            mapgame.npcs["caravan_leader_darek"].messages_morning = {
                0: ["Safe and sound in Epiiat, thanks to you. The goods are delivered, and the road is clear. Well "
                    "done, traveler."]}
            mapgame.npcs["caravan_leader_darek"].messages_evening = {
                0: ["Night falls heavy in this cavern, but at least we're safe for now. You've earned a rest,"
                    " traveler."]}
            mapgame.npcs["caravan_leader_darek"].place_morning = [(9, 5)]
            mapgame.npcs["caravan_leader_darek"].place_evening = [(9, 5), "inn", "main_room"]

            mapgame.npcs["caravenner_lorien"].messages_morning = {
                0: ["Ah, Epiiat... It's been too long. Feels good to be back. Thanks for making it happen, friend."]}
            mapgame.npcs["caravenner_lorien"].messages_evening = {
                0: ["Heh... y'know, every time I come to Epiiat, I feel... happy. It’s ‘cause of the mayor’s"
                    " daughter.",
                    "She’s... she’s wonderful. Don’t tell anyone, alright?"]}
            mapgame.npcs["caravenner_lorien"].place_morning = [(9, 4)]
            mapgame.npcs["caravenner_lorien"].place_evening = [(9, 5), "inn"]

            mapgame.npcs["jester_ralzo"].messages_morning = {
                0: ["Epiiat welcomes me once more! Time to lift spirits and stir laughter. Don’t miss my next act, "
                    "hero!"]}
            mapgame.npcs["jester_ralzo"].messages_night = {
                0: ["A cavern’s as good a stage as any! Care to join us, hero? Music brightens even the darkest"
                    " corners!"]}
            mapgame.npcs["jester_ralzo"].place_morning = [(9, 5)]
            mapgame.npcs["jester_ralzo"].place_night = [(9, 5), "inn"]

            player.events["caravan_arrive"] = True

    # Event Fisherman Marlin quests (7/9).
    if all([player.events["marlin_quests_4"],
            not player.events["marlin_quests_5"],
            mapgame.npcs["fisherman_marlin"].hist_messages[0]]):
        mapgame.npcs["fisherman_marlin"].reset_hist_messages()

        player.add_item(item="fishing_pole", quantity=1)
        player.add_item(item="marlins_fish_tuna", quantity=3)

        mapgame.npcs["fisherman_marlin"].messages = {
            0: ["Ah, have you managed to deliver those tunas to Gareth yet?",
                "I hope he’s gotten them by now. He's been waiting on those for quite some time. Let me know if you"
                "ran into any trouble!"]}

        mapgame.npcs["traveler_elinor"].messages = {
            0: ["Oh, greetings, traveler!",
                "I had planned to cross the sea on a ship, but it seems that won’t happen soon.",
                "The sailors are too wary to sail with a dragon sighted nearby... Can’t say I blame them."]}

        mapgame.npcs["traveler_elinor"].place = [(27, 14)]

        player.events["marlin_quests_5"] = True
        player.events["antinas_permission"] = True

    # Event Fisherman Marlin quests (8/9).
    if all([player.events["marlin_quests_5"],
            not player.events["marlin_quests_6"],
            mapgame.npcs["villager_gareth"].hist_messages[0]]):
        mapgame.npcs["fisherman_marlin"].reset_hist_messages()

        mapgame.npcs["villager_gareth"].messages = {
            0: ["Ah, it’s you again! Always good to see a friendly face around here. How's the journey treating "
                "you? Hopefully, the sea's been kinder today!"]}

        mapgame.npcs["fisherman_marlin"].messages = {
            0: ["Ah, you’ve delivered the tunas to Gareth! Thank you so much for handling that.",
                "He’s a good friend of mine, and I’m glad you could help. I owe you one, adventurer.",
                "If you ever need something from me, you know where to find me!"]}

        player.events["marlin_quests_6"] = True

        # Event Fisherman Marlin quests (9/9).
    if all([player.events["marlin_quests_6"],
            mapgame.npcs["fisherman_marlin"].hist_messages[0]]):
        mapgame.npcs["fisherman_marlin"].messages_morning = {
            0: ["Ah, it's a quiet day today. The sea's calm, but the fish are being stubborn.",
                "Still, there's always something peaceful about being near the water.",
                "If you’re ever in need of some good fish, you know where to find me."]}

    # Event batle with Dragon FireFrost after winning.
    if mapgame.npcs["dragon_firefrost"].hist_messages[0] and not player.events["dragon_win"]:
        play, menu, win = battle(player=player, enemy=copy.deepcopy(MOBS["dragon"]), map_game=mapgame)
        if win:
            # Dragon and valley.
            mapgame.npcs["dragon_firefrost"].messages = {
                0: ["Impressive. Today, the winds of fate favor you.",
                    "I yield. But heed my words, for when the stars align in a different cosmic dance, "
                    "I shall await you once more.",
                    "Until then, let the echoes of our encounter linger in the mountain breeze.",
                    "Farewell, " + player.name + ".",
                    "Until our destinies entwine again."]}

            mapgame.npcs["dragon_firefrost"].place = [(31, 31)]

            talk(npc=mapgame.npcs["dragon_firefrost"], player=player, map_game=mapgame)

            mapgame.map_settings[(11, 24)].description = ("Frozen valley, a pristine, snow-covered expanse where "
                                                          "frost-kissed silence reigns. Glistening ice formations "
                                                          "adorn the landscape, creating an ethereal and serene "
                                                          "winter tableau in nature's icy embrace.")
            mapgame.map_settings[(11, 24)].npc = []

            mapgame.map_settings[(0, 0)].entries["hut"].items.append("origami_flowers")
            mapgame.npcs["dragon_firefrost"].place = None

            # Antinas NPCs.
            mapgame.npcs["marquis_edrion"].messages_morning = {
                0: ["At last, the dragon has departed! Perhaps now we can breathe easier and rebuild our strength. "
                    "These lands have endured enough turmoil."]}

            mapgame.npcs["lord_aric"].messages_morning = {
                0: ["Ah, the dragon is gone at last! But what could have driven it away? Such a mystery...",
                    "Yet, I suppose we should be grateful all the same."]}

            mapgame.npcs["villager_fenna"].messages_morning = {
                0: ["The dragon left? How strange... I guess some things are meant to be.",
                    "It would’ve been something to see it up close, but maybe it’s better this way."]}
            mapgame.npcs["villager_fenna"].messages_evening = None
            mapgame.npcs["villager_fenna"].messages_night = {
                0: ["Zzz... zzz... zzz..."]}

            mapgame.npcs["villager_garrek"].messages_morning = {
                0: ["The animals are finally calm again. The dragon’s gone, but the memories of those tense days will "
                    "stick with me for a while.",
                    "Glad we made it through."]}
            mapgame.npcs["villager_garrek"].messages_evening = None
            mapgame.npcs["villager_garrek"].messages_night = {
                0: ["Zzz... zzz... zzz... Snore..."]}

            mapgame.npcs["villager_halden"].messages_morning = {
                0: ["Well, it seems like the storm has passed. I knew the kingdom's protectors wouldn't let us down.",
                    "I’ll sleep easier tonight, that’s for sure."]}
            mapgame.npcs["villager_halden"].messages_evening = {
                0: ["It feels good knowing the danger has passed. I'll sleep soundly tonight, for the first time"
                    " in days.",
                    "The air even feels calmer, like the world itself can finally breathe again."]}
            mapgame.npcs["villager_halden"].messages_night = None

            mapgame.npcs["villager_lyria"].messages_morning = {
                0: ["I can't believe it's over... The dragon's gone? I don't know whether to feel relieved"
                    " or... disappointed.",
                    "It's strange, the air feels lighter now."]}
            mapgame.npcs["villager_lyria"].messages_evening = {
                0: ["I’m so glad it’s finally over... The dragon’s gone, and I can finally get some rest.",
                    "It was a long, sleepless week. Now, I can sleep without worrying if we'll be next."]}

            mapgame.npcs["villager_mirrel"].messages_morning = {
                0: ["Thank the gods, it's gone... but I can't help but wonder if we'll be safe for long.",
                    "Something tells me we’ve just gotten lucky."]}
            mapgame.npcs["villager_mirrel"].messages_evening = {
                0: ["I don’t know if I’ll ever fully forget those days... But I’m glad it’s behind us now.",
                    "Time to rest and let the fear drift away, like the dragon."]}

            mapgame.npcs["villager_orik"].messages_morning = {
                0: ["Huh, the dragon's gone? Guess it's back to work then.",
                    "Not that I’m complaining—this place is peaceful again. At least for now.",
                    "Glad we made it through."]}
            mapgame.npcs["villager_orik"].messages_night = None
            mapgame.npcs["villager_orik"].messages_night = {
                0: ["Hmmm... Hmmm... Zzzzz..."]}

            mapgame.npcs["captain_thorne"].messages_morning = {
                0: ["Ahoy, traveler! With the skies clear and the dragon gone, we’re ready to set sail east to "
                    "the port city of Veylan.",
                    "I’m Captain Thorne—prepare yourself, the journey awaits!"]}
            mapgame.npcs["captain_thorne"].reset_hist_messages()

            mapgame.npcs["whispers"].messages = {
                0: [f"The dream has ended, {player.name}.",
                    "Veylan opens a world of possibilities—if you’re ready to see them."]}

            player.add_item(item="dragon_scales", quantity=8)
            player.events["dragon_win"] = True

            return play, menu

        else:
            mapgame.npcs["dragon_firefrost"].reset_hist_messages()
            save(player=player, mapgame=mapgame, time_init=time_init)
            return play, menu

    # Event captain Thorne travel.
    if mapgame.npcs["captain_thorne"].hist_messages[0] and player.events["dragon_win"]:
        utils.clear()
        time.sleep(1.5)
        talk(npc=mapgame.npcs["whispers"], player=player, map_game=mapgame)

        return False, True

    return True, False


def import_player(path: str) -> Player | None:
    try:
        with open(path, 'rb') as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:
        return None


def import_map(path: str) -> Map | None:
    try:
        with open(path, 'rb') as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:
        return None


def map_control_handling(player: Player,
                         mapgame: Map):
    # Control of Innkeeper room expirations.
    for npc in player.place.npc:
        if mapgame.npcs[npc].npc_type == NpcTypes.INNKEEPER:
            expirated_room_keys = mapgame.check_room_expiration(player=player, npc=npc)
            for key in expirated_room_keys:
                player.inventory.drop_item(item=key, quantity=player.inventory.items[key])
                disp_talk_tw(npc=mapgame.npcs[npc],
                             message=["Ah, there you are. Your stay was pleasant, I hope. But your days are up, "
                                      "traveler. I’ll need the room key back now. Don’t worry—you’re welcome to rent "
                                      "it again if you plan on staying longer."])

            for key in expirated_room_keys:
                del mapgame.npcs[npc].room_expirations[key]

    # Sailor Kael detention.
    if "sailor_kael" in player.place.npc and player.place == mapgame.map_settings[(27, 15)].entries["thornes_ship"]:
        talk(npc=mapgame.npcs["sailor_kael"], player=player, map_game=mapgame)
        player.set_place(place=player.last_place)

    # Guard Lorian ddetention.
    if "guard_lorian" in player.last_place.npc and player.place == mapgame.map_settings[(12, 17)]:
        if not player.events["antinas_permission"]:
            talk(npc=mapgame.npcs["guard_lorian"], player=player, map_game=mapgame)
            player.set_place(place=player.last_place)


def load(path_usavepkl: str = "cfg_save.pkl",
         path_msave: str = "cfg_map.pkl",
         path_hsave: str = "cfg_hash.txt",
         check_hash: bool = True) -> tuple[bool, str, Player | None, Map | None]:
    """Checks corruption of files and finally loads game."""
    if check_hash:
        load_hash = utils.load_dict_from_txt(path_hsave)
        if not utils.get_hash("cfg_save.pkl") == load_hash["hash"]:
            return False, " Corrupted file.", None, None

    player = import_player(path_usavepkl)
    mapgame = import_map(path_msave)

    if player is None:
        return False, " Player have been not found.", None, None

    if mapgame is None:
        return False, " Player map file have been not found.", None, None

    return True, f" Welcome back {player.name}.", player, mapgame


def reinit(player: Player, mapgame: Map):
    # Player reinit.
    player.hp = int(player.hpmax)
    player.x = player.x_cp
    player.y = player.y_cp
    player.status = 0
    player.poison = 0
    player.hungry = 48
    player.thirsty = 48
    player.exp = 0

    # Map reinit.
    utils.reset_map(ms=mapgame.map_settings,
                    keys=[(2, 1), (6, 2)])


def repair(player: Player, mapgame: Map):
    pass


# Save function.
def save(player: Player,
         mapgame: Map,
         time_init: datetime,
         path_usavepkl: str = "cfg_save.pkl",
         path_mappkl: str = "cfg_map.pkl",
         path_hsave: str = "cfg_hash.txt") -> None:
    """Saves game."""
    player.refresh_time_played(datetime.now(), time_init)

    # Inventory, user stats and map setting saving (export to txt).
    utils.export_player(player, path_usavepkl)
    utils.export_player(mapgame, path_mappkl)

    # Hash saving (export to dict).
    utils.export_dict_to_txt(dictionary={"hash": utils.get_hash(path_usavepkl)}, file_path=path_hsave)


def update(player: Player,
           mapgame: Map,
           option: str) -> tuple[str, Player, Map]:
    """
    Updates class Player and class Map.
    """
    if option == "map_npcs":
        mapgame.npcs = globals.NPCS.copy()
        return "Update NPCS MAP succesfully.", player, mapgame

    if option == "map_mobs":
        mapgame.mobs = globals.MOBS.copy()
        return "Update MOBS MAP succesfully.", player, mapgame

    if option == "player":
        new_player = Player(name=player.name,
                            hp=player.hp,
                            lvl=player.lvl,
                            exp=player.exp,
                            expmax=player.expmax,
                            hungry=player.hungry,
                            thirsty=player.thirsty,
                            status=player.status,
                            poison=player.poison,
                            freezing=player.freezing,
                            b_hpmax=player.b_hpmax,
                            b_attack=player.b_attack,
                            b_defense=player.b_defense,
                            b_evasion=player.b_evasion,
                            b_precision=player.b_precision,
                            b_weight_carry=player.b_weight_carry,
                            strength=player.strength,
                            resistance=player.resistance,
                            agility=player.agility,
                            vitality=player.vitality,
                            dexterity=player.dexterity,
                            attack_factor=player.attack_factor,
                            defence_factor=player.defence_factor,
                            evasion_factor=player.evasion_factor,
                            precision_factor=player.precision_factor,
                            vitality_factor=player.vitality_factor,
                            vision=player.vision,
                            x=player.x,
                            y=player.y,
                            x_cp=player.x_cp,
                            y_cp=player.y_cp,
                            outside=player.outside,
                            place=player.place,
                            last_place=player.last_place,
                            last_entry=player.last_entry,
                            st_points=player.st_points,
                            sk_points=player.sk_points,
                            inventory=player.inventory,
                            slot1=player.slot1,
                            slot2=player.slot2,
                            equip=player.equip,
                            map=player.map,
                            events=player.events,
                            time_played=player.time_played)
        return "Player class updated.", new_player, mapgame

    if option == "map_13_0":
        sub_cave_2_3 = ENTRIES["sub_cave_2_3"]
        sub_cave_3_1 = ENTRIES["sub_cave_3_1"]
        mapgame.map_settings[(13, 0)].entries["big_cave"].entries["passageway_cave_entrance"].entries[
            "goblin_dining_gallery"].entries = {"cave_passageway_entrance": sub_cave_2_3,
                                                "cave_passageway_exit": sub_cave_3_1}
        return "Update MAP 13 0 succesfully.", player, mapgame

    return "Nothing done.", player, mapgame
