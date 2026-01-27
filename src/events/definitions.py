# Imports.
# Local imports.
from ..actions.actions import battle
from ..actions.talk import talk
from .. import displays
from ..enums import TimeOfDay
from .events import Event
from ..map import Map
from ..player import Player
from .timer import Timer

# External imports
import copy


# Starter events.
def call_completed_exit_the_hut(player: Player, mapgame: Map, update: bool = False) -> None:
    if not update:
        displays.disp_narration()
        talk(npc=mapgame.npcs["islander_nynaeve"], player=player, mapgame=mapgame)

    player.remove_quest(quest="quest_exit_the_hut")

    mapgame.npcs["islander_nynaeve"].clear_messages_answers()
    mapgame.npcs["islander_nynaeve"].messages_morning = {
        0: [
            "Hello, dear one.",
            "Tell me… are you hungry?",
            "If so, ENTER and have some soup.",
            "There’s a warm pot waiting for you."
        ]
    }

    mapgame.npcs["islander_nynaeve"].place_morning = [(12, 24)]

    mapgame.npcs["islander_nynaeve"].messages_night = {
        0: [
            "Dear one.",
            "Tell me… are you hungry?",
            "I’ve kept a warm pot ready for you."
        ]
    }

    mapgame.refresh_npcs()

    mapgame.map_settings[(12, 24)].entries["hut"].items.append("soup")
    player.add_quest(quest=mapgame.quests["quest_eat_soup"])


event_completed_exit_the_hut = Event(
    id="event_completed_exit_the_hut",
    action=call_completed_exit_the_hut
)


def call_completed_eat_soup(player: Player, mapgame: Map, update: bool = False) -> None:
    player.remove_quest(quest="quest_eat_soup")
    mapgame.npcs["islander_nynaeve"].add_quest(quest=mapgame.quests["quest_find_loial"])


event_completed_eat_soup = Event(
    id="event_completed_eat_soup",
    action=call_completed_eat_soup
)


def call_completed_find_loial(player: Player, mapgame: Map, update: bool = False) -> None:
    mapgame.npcs["islander_nynaeve"].clear_messages_answers()

    mapgame.npcs["islander_nynaeve"].messages_morning = {
        0: [
            "Good morning!",
            "How are you feeling today?"
        ]
    }
    mapgame.npcs["islander_nynaeve"].answers_morning = {}

    mapgame.npcs["islander_nynaeve"].messages_afternoon = {
        0: [
            "You seem full of energy.",
            "If you have time, maybe Loial could use a hand with the island tasks."
        ]
    }
    mapgame.npcs["islander_nynaeve"].answers_afternoon = {}

    mapgame.npcs["islander_nynaeve"].messages_evening = {
        0: [
            "You know… we were very worried when we found you lying on the beach.",
            "It’s a relief to see you standing strong now."
        ],
        1: ["We found you a few days ago, badly wounded.",
            "We took care of you until you finally woke up.",
            "Mmm… still having trouble with your memory?"],
        2: [
            "There’s an old boat Loial uses to reach the village of Epiiat, but I believe it’s broken.",
            "You should talk to him—he sensed you’d want to leave soon."
        ],
    }
    mapgame.npcs["islander_nynaeve"].answers_evening = {
        1: "How was I found on the beach?",
        2: "Do you know how I can leave the island?"
    }
    mapgame.npcs["islander_nynaeve"].messages_night = {
        0: [
            "It’s been a long day.",
            "We should all get some rest."
        ]
    }
    mapgame.npcs["islander_nynaeve"].answers_night = {}

    mapgame.npcs["islander_loial"].add_quest(quest=mapgame.quests["quest_deliver_wood"])

    mapgame.refresh_npcs()


event_completed_find_loial = Event(
    id="event_completed_find_loial",
    action=call_completed_find_loial
)


def call_started_deliver_wood(player: Player, mapgame: Map, update: bool = False) -> None:
    mapgame.npcs["islander_nynaeve"].clear_messages_answers()

    mapgame.npcs["islander_nynaeve"].messages_morning = {
        0: [
            "Good morning! Oh—did you really bring the wood?",
            "Loial mentioned he needed it, but I didn’t expect you to be so quick!"
        ]
    }
    mapgame.npcs["islander_nynaeve"].messages_afternoon = {
        0: [
            "Oh! You’re here—and with the wood?",
            "I wasn’t expecting it. This will help Loial a lot, thank you."
        ]
    }
    mapgame.npcs["islander_nynaeve"].messages_evening = {
        0: [
            "You brought the wood…?",
            "I’m surprised—pleasantly surprised. Loial will be grateful."
        ]
    }

    mapgame.npcs["islander_nynaeve"].messages_night = {
        0: [
            "Out this late… and you still came with the wood?",
            "You really went out of your way. Loial will make good use of it—thank you."
        ]
    }

    mapgame.refresh_npcs()


event_started_find_loial = Event(
    id="event_started_find_loial",
    action=call_started_deliver_wood
)


def call_completed_deliver_wood(player: Player, mapgame: Map, update: bool = False) -> None:
    mapgame.npcs["islander_nynaeve"].clear_messages_answers()

    mapgame.npcs["islander_nynaeve"].messages_morning = {
        0: [
            "Good morning!",
            "How are you feeling today?"
        ]
    }
    mapgame.npcs["islander_nynaeve"].answers_morning = {}

    mapgame.npcs["islander_nynaeve"].messages_afternoon = {
        0: [
            "You seem full of energy.",
            "If you have time, maybe Loial could use a hand with the island tasks."
        ]
    }
    mapgame.npcs["islander_nynaeve"].answers_afternoon = {}

    mapgame.npcs["islander_nynaeve"].messages_evening = {
        0: [
            "You know… we were very worried when we found you lying on the beach.",
            "It’s a relief to see you standing strong now."
        ],
        1: ["We found you a few days ago, badly wounded.",
            "We took care of you until you finally woke up.",
            "Mmm… still having trouble with your memory?"],
        2: [
            "There’s an old boat Loial uses to reach the village of Epiiat, but I believe it’s broken.",
            "You should talk to him—he sensed you’d want to leave soon."
        ],
    }
    mapgame.npcs["islander_nynaeve"].answers_evening = {
        1: "How was I found on the beach?",
        2: "Do you know how I can leave the island?"
    }
    mapgame.npcs["islander_nynaeve"].messages_night = {
        0: [
            "It’s been a long day.",
            "We should all get some rest."
        ]
    }
    mapgame.npcs["islander_nynaeve"].answers_night = {}

    mapgame.npcs["islander_nynaeve"].place_morning = [(12, 24)]
    mapgame.npcs["islander_nynaeve"].place_afternoon = [(12, 24)]
    mapgame.npcs["islander_nynaeve"].place_evening = [(12, 24)]
    mapgame.npcs["islander_nynaeve"].place_night = [(12, 24), "hut"]

    mapgame.npcs["islander_loial"].place_morning = [(12, 24)]
    mapgame.npcs["islander_loial"].place_afternoon = [(12, 24), "hut"]
    mapgame.npcs["islander_loial"].place_evening = [(12, 24)]
    mapgame.npcs["islander_loial"].place_night = [(12, 24), "hut", "nynaeve_room"]

    mapgame.npcs["islander_loial"].add_quest(quest=mapgame.quests["slime_slayer_I"])
    mapgame.npcs["islander_loial"].add_quest(quest=mapgame.quests["slime_slayer_II"])

    mapgame.refresh_npcs()


event_completed_deliver_wood = Event(
    id="event_completed_deliver_wood",
    action=call_completed_deliver_wood
)


def call_completed_slime_slayer_I(player: Player, mapgame: Map, update: bool = False) -> None:
    if mapgame.get_number_of_mobs(coord1=(11, 23), coord2=(13, 25), mob_id="little_slime") <= 5:
        mapgame.map_settings[(11, 23)].respawn_mob(mob="little_slime", amount=2)
        mapgame.map_settings[(12, 23)].respawn_mob(mob="little_slime", amount=2)
        mapgame.map_settings[(11, 23)].respawn_mob(mob="little_slime", amount=2)


event_completed_slime_slayer_I = Event(
    id="event_completed_slime_slayer_I",
    action=call_completed_slime_slayer_I
)


def timer_call_loial_repair_boat(mapgame: Map, **kwargs):
    mapgame.npcs["islander_loial"].clear_messages_answers()
    mapgame.npcs["islander_loial"].messages_morning = {
        0: [
            "Another day at the lumberyard… I really should sharpen my axe.",
            "Work goes faster when the tools are in good shape.",
            "I’d love to visit the waterfall with Nynaeve once I’m done here."
        ]
    }

    mapgame.npcs["islander_loial"].messages_afternoon = {
        0: [
            "Mmm… this soup is delicious.",
            "Nynaeve really knows how to cook."
        ]
    }

    mapgame.npcs["islander_loial"].messages_evening = {
        0: [
            "What a lovely night… so calm and warm.",
            "Both moons are shining brighter than usual."
        ]
    }

    mapgame.npcs["islander_loial"].messages_night = {
        0: [
            "Mmmhh… so cozy…",
            "Hooom… zzz… mmmm…"
        ]
    }

    mapgame.npcs["islander_loial"].place_morning = [(13, 23)]
    mapgame.npcs["islander_loial"].place_afternoon = [(12, 24), "hut"]
    mapgame.npcs["islander_loial"].place_evening = [(12, 24)]
    mapgame.npcs["islander_loial"].place_night = [(12, 24), "hut", "nynaeve_room"]

    displays.clear()
    mapgame.map_settings[(14, 25)].add_item(item_id="boat")
    mapgame.map_settings[(14, 25)].remove_item(item="broken_boat")
    mapgame.map_settings[(14, 25)].add_item(item_id="apple")
    mapgame.map_settings[(14, 25)].reinit_items = {"boat": 1}

    mapgame.refresh_npcs()


def call_rewarded_slime_slayer_II(player: Player, mapgame: Map, update: bool = False) -> None:
    mapgame.npcs["islander_loial"].clear_messages_answers()
    mapgame.npcs["islander_loial"].messages_morning = {
        0: [
            "Waking up early always makes the work smoother.",
            "If everything goes well, the boat should be fully repaired in about three days."
        ]
    }

    mapgame.npcs["islander_loial"].messages_afternoon = {
        0: [
            "I’ll work a little longer before taking a break.",
            "Nynaeve prepared lunch for me—can’t wait to sit down and enjoy it."
        ]
    }

    mapgame.npcs["islander_loial"].messages_evening = {
        0: [
            "The day’s been long, but I made good progress on the boat.",
            "A quiet evening like this helps me clear my mind."
        ]
    }

    mapgame.npcs["islander_loial"].messages_night = {
        0: [
            "Mmm… so tired…",
            "Zzzzz… zzz-hhh…"
        ]
    }

    mapgame.npcs["islander_loial"].place_morning = [(14, 25)]
    mapgame.npcs["islander_loial"].place_afternoon = [(14, 25)]
    mapgame.npcs["islander_loial"].place_evening = [(12, 24), "hut"]
    mapgame.npcs["islander_loial"].place_night = [(12, 24), "hut", "nynaeve_room"]

    mapgame.refresh_npcs()

    if not update:
        mapgame.add_timer(timer=Timer(
            id="loial_repair_boat",
            duration=3,
            on_finish=timer_call_loial_repair_boat,
            day=mapgame.current_day,
            month=mapgame.current_month,
            year=mapgame.current_year
        ))
    else:
        timer_call_loial_repair_boat(mapgame=mapgame)


event_rewarded_slime_slayer_II = Event(
    id="event_rewarded_slime_slayer_II",
    action=call_rewarded_slime_slayer_II
)


# Epiiat events.
def trigger_goblin_chief_battle(player: Player, mapgame: Map, update: bool = False) -> bool:
    quest = player.get_quest(quest_id="quest_goblin_chief")
    if quest is None or quest.is_in_progress():
        return player.place.id == "goblin_chief_bedroom"
    return False


def timer_mayors_daughter_maisie_return(mapgame: Map, **kwargs):
    mapgame.npcs["mayors_daughter_maisie"].clear_messages_answers()

    mapgame.npcs["mayors_daughter_maisie"].messages = {
        0: ["Thank you, brave one!",
            "If not for your help, I might have tried to escape through one of the hidden passages in the cave.",
            "I saw them but had no chance to explore. Your courage saved me before I could take the risk.",
            "I owe you my life."]}

    mapgame.npcs["mayors_daughter_maisie"].place_morning = [(22, 28)]
    mapgame.npcs["mayors_daughter_maisie"].place_evening = [(22, 28), "mayors_house"]

    mapgame.npcs["villager_merrin"].messages = {
        0: ["You did it! You brought Maisie back safely. I can’t thank you enough.",
            "The whole village has been in distress since she went missing. You’ve given us hope again, brave one.",
            "We’ll not forget what you’ve done for Epiiat."]}
    mapgame.npcs["villager_fira"].messages = {
        0: ["I just heard the news—Maisie is safe and back home. What a blessing for the whole village.",
            "We’ve all been on edge since she went missing. It feels like a dark cloud has finally "
            "lifted from Epiiat."]}

    mapgame.refresh_npcs()


def call_goblin_chief_battle(player: Player, mapgame: Map, update: bool = False) -> bool | None:
    win = True
    if not update:
        talk(npc=mapgame.npcs["goblin_griznuk"], player=player, mapgame=mapgame)
        win = battle(players=[player], enemies=[copy.deepcopy(mapgame.mobs["goblin_chief"])], mapgame=mapgame)

    if not win:
        return

    if not update:
        talk(npc=mapgame.npcs["mayors_daughter_maisie"], player=player, mapgame=mapgame)

    mapgame.npcs["mayors_daughter_maisie"].clear_messages_answers()
    mapgame.npcs["mayors_daughter_maisie"].messages = {
        0: ["My father, the mayor, will want to thank you properly. Please, come back with me to the village.",
            "Words cannot express my gratitude, but I hope our people can repay your bravery."]}
    mapgame.refresh_npcs()

    if not player.has_quest(quest="quest_goblin_chief"):
        player.add_quest(quest=mapgame.quests["quest_goblin_chief"])
        player.get_quest(quest_id="quest_goblin_chief").complete_quest()

    if not update:
        mapgame.add_timer(
            timer=Timer(
                id="mayors_daughter_maisie_return",
                duration=4,
                on_finish=timer_mayors_daughter_maisie_return,
                day=mapgame.current_day,
                month=mapgame.current_month,
                year=mapgame.current_year
            )
        )
    else:
        timer_mayors_daughter_maisie_return(mapgame=mapgame)

    return True


event_goblin_chief_battle = Event(
    id="event_goblin_chief_battle",
    action=call_goblin_chief_battle,
    trigger=trigger_goblin_chief_battle,
    one_execution=False
)


def call_completed_goblin_chief(player: Player, mapgame: Map, update: bool = False) -> None:
    cave_passageway_exit = mapgame.place_from_list([(25, 24),
                                                    "cave_entrance",
                                                    "cave_pit",
                                                    "cave_basin",
                                                    "cave_gallery",
                                                    "cave_passageway_exit"])
    cave_passageway_exit.entries["chimney"] = mapgame.entries["sub_cave_4_0"]
    chimney = mapgame.entries["sub_cave_4_0"]
    chimney.entries = {"cave_passageway_exit": cave_passageway_exit,
                       "surface": mapgame.map_settings[(31, 24)]}


event_completed_goblin_chief = Event(
    id="event_completed_goblin_chief",
    action=call_completed_goblin_chief
)


def call_rewarded_goblin_chief(player: Player, mapgame: Map, update: bool = False) -> None:
    mapgame.npcs["mayor_thorian"].messages = {
        0: [
            "It’s rare to find such selfless bravery in these dark times. Thanks to you, my daughter is "
            "safe, and Epiiat breathes easier tonight.",
            "I must ensure the village knows of this deed; tales of courage like this must be remembered.",
            "May the gods guide that your steps, wherever the road may lead."
        ]
    }

    mapgame.refresh_npcs()


event_rewarded_goblin_chief = Event(
    id="event_rewarded_goblin_chief",
    action=call_rewarded_goblin_chief
)


# Aquiri events.
def call_started_quest_marlin_fish_for_brann(player: Player, mapgame: Map, update: bool = False) -> None:
    mapgame.npcs["fisherman_brann"].clear_messages_answers()

    mapgame.npcs["fisherman_brann"].messages = {
        0: [
            "Oh, by the tides! You’ve brought Marlin’s tuna, haven’t you? I wasn’t sure he’d manage to send it.",
            "Thank you, traveler! This means more to me than you know."
        ]
    }

    mapgame.npcs["fisherman_brann"].messages_morning = {
        0: [
            "Oh, by the tides! You’ve brought Marlin’s tuna, haven’t you? I wasn’t sure he’d manage to send it.",
            "Thank you, traveler! This means more to me than you know."
        ]
    }

    mapgame.refresh_npcs()


event_started_quest_marlin_fish_for_brann = Event(
    id="event_started_quest_marlin_fish_for_brann",
    action=call_started_quest_marlin_fish_for_brann
)


def call_completed_quest_marlin_fish_for_brann(player: Player, mapgame: Map, update: bool = False) -> None:
    mapgame.npcs["fisherman_brann"].clear_messages_answers()

    mapgame.npcs["fisherman_brann"].messages = {
        0: [
            "Ah, traveler! Good to see you again.",
            "Thanks to you, Marlin’s tuna was a real treat. How’s the road treating you?"
        ]
    }

    mapgame.npcs["caravan_leader_darek"].place = [(28, 29)]
    mapgame.npcs["caravenner_lorien"].place = [(28, 29)]
    mapgame.npcs["jester_ralzo"].place = [(28, 29)]
    mapgame.npcs["traveler_kaelen"].place = [(28, 29)]

    mapgame.refresh_npcs()


event_completed_quest_marlin_fish_for_brann = Event(
    id="event_completed_quest_marlin_fish_for_brann",
    action=call_completed_quest_marlin_fish_for_brann
)


def call_completed_quest_find_caravan_leader_darek(player: Player, mapgame: Map, update: bool = False) -> None:
    pass


event_completed_quest_find_caravan_leader_darek = Event(
    id="event_completed_quest_find_caravan_leader_darek",
    action=call_completed_quest_find_caravan_leader_darek
)


def timer_caravan_move(mapgame: Map, **kwargs):
    mapgame.npcs["caravan_leader_darek"].messages_morning = {
        0: ["Safe and sound in Epiiat, thanks to you. The goods are delivered, and the road is clear. Well "
            "done, traveler."]}
    mapgame.npcs["caravan_leader_darek"].messages_evening = {
        0: ["Night falls heavy in this cavern, but at least we're safe for now. You've earned a rest,"
            " traveler."]}
    mapgame.npcs["caravan_leader_darek"].place_morning = [(21, 29)]
    mapgame.npcs["caravan_leader_darek"].place_evening = [(21, 29), "inn", "main_room"]

    mapgame.npcs["caravenner_lorien"].messages_morning = {
        0: ["Ah, Epiiat... It's been too long. Feels good to be back. Thanks for making it happen, friend."]}
    mapgame.npcs["caravenner_lorien"].messages_evening = {
        0: ["Heh... y'know, every time I come to Epiiat, I feel... happy. It’s ‘cause of the mayor’s"
            " daughter.",
            "She’s... she’s wonderful. Don’t tell anyone, alright?"]}
    mapgame.npcs["caravenner_lorien"].place_morning = [(21, 28)]
    mapgame.npcs["caravenner_lorien"].place_evening = [(21, 29), "inn"]

    mapgame.npcs["jester_ralzo"].messages_morning = {
        0: ["Epiiat welcomes me once more! Time to lift spirits and stir laughter. Don’t miss my next act, "
            "hero!"]}
    mapgame.npcs["jester_ralzo"].messages_night = {
        0: ["A cavern’s as good a stage as any! Care to join us, hero? Music brightens even the darkest"
            " corners!"]}
    mapgame.npcs["jester_ralzo"].place_morning = [(21, 29)]
    mapgame.npcs["jester_ralzo"].place_night = [(21, 29), "inn"]

    mapgame.npcs["traveler_kaelen"].messages_morning = {
        0: [
            "Ah, traveler… welcome.",
            "These ruins may seem quiet, but do not be fooled. Their stones hold whispers of ages long gone.",
            "If you take the time to look closely—really look—you may find traces of stories forgotten by most.",
            "Symbols worn by wind, carvings hidden beneath the moss… all waiting for someone with keen eyes and a "
            "curious spirit.",
            "Most people walk past without noticing a thing.",
            "But the past lingers here, patient and silent, ready to reveal itself to those who listen."
        ]
    }
    mapgame.npcs["traveler_kaelen"].place_morning = [(5, 41)]

    mapgame.refresh_npcs()


def call_completed_quest_destroy_rocks_on_valley(player: Player, mapgame: Map, update: bool = False) -> None:
    mapgame.npcs["caravan_leader_darek"].clear_messages_answers()
    mapgame.npcs["caravan_leader_darek"].messages = {
        0: ["You’ve done us a great service, adventurer! Thanks to you, the road is clear, and we can finally "
            "make our way to Epiiat. Safe travels, friend!"]}

    mapgame.npcs["caravenner_lorien"].clear_messages_answers()
    mapgame.npcs["caravenner_lorien"].messages = {
        0: ["At last, I’ll see Epiiat again! Thank you, traveler. It’s been too long since I walked its streets."]}

    mapgame.npcs["jester_ralzo"].clear_messages_answers()
    mapgame.npcs["jester_ralzo"].messages = {
        0: ["Oh, glorious news! Back to Epiiat I go, ready to dazzle with my finest show! Care to attend,"
            " traveler?"]}

    mapgame.npcs["traveler_kaelen"].clear_messages_answers()
    mapgame.npcs["traveler_kaelen"].messages = {
        0: ["Well done, traveler! You’ve handled that kegpowder with real skill. Not everyone could pull that off.",
            "The road's better thanks to you!"]}

    mapgame.npcs["worker_gorrick"].clear_messages_answers()
    mapgame.npcs["worker_gorrick"].messages = {
        0: ["Finally, the valley is cl...",
            "Zzzz... Zzz..."]}

    mapgame.npcs["worker_gorrick"].place = [(22, 28), "wooden_house"]

    mapgame.refresh_npcs()

    if not update:
        mapgame.add_timer(
            timer=Timer(
                id="mayors_daughter_maisie_return",
                duration=3,
                on_finish=timer_caravan_move,
                day=mapgame.current_day,
                month=mapgame.current_month,
                year=mapgame.current_year
            )
        )
    else:
        timer_caravan_move(mapgame=mapgame)


event_completed_quest_destroy_rocks_on_valley = Event(
    id="event_completed_quest_destroy_rocks_on_valley",
    action=call_completed_quest_destroy_rocks_on_valley
)


def call_completed_quest_gareth_deliver(player: Player, mapgame: Map, update: bool = False) -> None:
    mapgame.npcs["villager_gareth"].clear_messages_answers()
    mapgame.npcs["villager_gareth"].messages = {
        0: ["Ah, it’s you again! Always good to see a friendly face around here. How's the journey treating "
            "you? Hopefully, the sea's been kinder today!"]}


event_completed_quest_gareth_deliver = Event(
    id="event_completed_quest_gareth_deliver",
    action=call_completed_quest_gareth_deliver
)


# FireFrost first encounter.
def trigger_firefrost_first_encounter_battle(player: Player, mapgame: Map, update: bool = False) -> bool:
    quest = player.get_quest(quest_id="quest_firefrost_first_encounter")
    if quest is None or quest.is_in_progress():
        return player.place.id == "frostvale"
    return False


def call_firefrost_first_encounter_battle(player: Player, mapgame: Map, update: bool = False) -> bool | None:
    win = True
    if not update:
        talk(npc=mapgame.npcs["dragon_firefrost"], player=player, mapgame=mapgame)
        win = battle(players=[player],
                     enemies=[copy.deepcopy(mapgame.mobs["dragon"])],
                     mapgame=mapgame,
                     data_battle={"mob_life_limit": 20})

    if not win:
        return

    return True


event_firefrost_first_encounter_battle = Event(
    id="event_firefrost_first_encounter_battle",
    action=call_firefrost_first_encounter_battle,
    trigger=trigger_firefrost_first_encounter_battle,
    one_execution=False,
)


def call_completed_quest_firefrost_first_encounter(player: Player, mapgame: Map, update: bool = False) -> None:
    # FireFrost changes.
    mapgame.npcs["dragon_firefrost"].clear_messages_answers()
    displays.disp_standard_tw(
        name="Dragon FireFrost",
        message=[
            "Impressive. Today, the winds of fate favor you.",
            "I yield. But heed my words, for when the stars align in a different cosmic dance, "
            "I shall await you once more.",
            "Until then, let the echoes of our encounter linger in the mountain breeze.",
            "Farewell, " + player.name + ".",
            "Until our destinies entwine again."
        ]
    )

    # Npc changes.
    # Antina npcs.
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

    # Aquiri npcs.
    mapgame.npcs["captain_thorne"].messages_morning = {
        0: [
            "Ahoy, traveler. I'm Captain Thorne.",
            "The seas look calmer today, and that dragon hasn't shown itself since dawn.",
            "If you’re looking to leave port, I can take you—my crew is ready to set sail whenever you are.",
            "Just say the word, and we’ll chart a course to the next harbor."
        ],
        1: ["Where will the wind take us?"]
    }

    mapgame.npcs["captain_thorne"].messages_evening = {
        0: [
            "Evening, traveler. The crew’s getting some rest before we depart at first light.",
            "If you need passage, find me in the morning—I'll have the ship ready to sail."
        ]
    }
    mapgame.npcs["captain_thorne"].add_transport_place(place_coordinate=(39, 39), place_price={"gold": 20, "days": 10})
    mapgame.npcs["captain_thorne"].add_transport_place(place_coordinate=(56, 40), place_price={"gold": 20, "days": 10})
    mapgame.npcs["captain_thorne"].transport_time_of_day = [TimeOfDay.MORNING.value, TimeOfDay.AFTERNOON.value]
    mapgame.npcs["captain_thorne"].transport_confirm_message = ["Are you sure you want to go there?"]
    mapgame.npcs["captain_thorne"].transport_arrive_message = ["Finally, we have arrived. Take care, and may Eldra "
                                                               "watch over you."]
    mapgame.npcs["captain_thorne"].answers = {1: "I want to sail"}

    mapgame.refresh_npcs()

    # Reward.
    player.add_item(item="dragon_scales", quantity=8)
    player.remove_quest(quest="quest_firefrost_first_encounter")

    # Other changes.
    mapgame.map_settings[(12, 24)].entries["hut"].entries["little_room"].items.append("origami_flowers")


event_completed_quest_firefrost_first_encounter = Event(
    id="event_completed_quest_firefrost_first_encounter",
    action=call_completed_quest_firefrost_first_encounter,
)


# Veylan events.
def call_quest_complete_explore_veylan(player: Player, mapgame: Map, update: bool = False) -> None:
    displays.disp_standard_tw(
        name="Whispers",
        message=[
            "Soon… our paths will cross again beneath shifting skies.",
            "Until that moment, tread lightly—Aerthos hides many perils, and Thelm… far darker still."
        ]
    )


event_completed_quest_complete_explore_veylan = Event(
    id="event_completed_quest_complete_explore_veylan",
    action=call_quest_complete_explore_veylan,
)


# Events list.
EVENTS = [
    event_completed_exit_the_hut,
    event_completed_eat_soup,
    event_started_find_loial,
    event_completed_find_loial,
    event_completed_deliver_wood,
    event_completed_slime_slayer_I,
    event_rewarded_slime_slayer_II,

    event_goblin_chief_battle,
    event_completed_goblin_chief,
    event_rewarded_goblin_chief,

    event_started_quest_marlin_fish_for_brann,
    event_completed_quest_marlin_fish_for_brann,
    event_completed_quest_find_caravan_leader_darek,
    event_completed_quest_destroy_rocks_on_valley,
    event_completed_quest_gareth_deliver,

    event_firefrost_first_encounter_battle,
    event_completed_quest_firefrost_first_encounter,

    event_completed_quest_complete_explore_veylan,
]
