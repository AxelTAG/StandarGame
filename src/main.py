# Imports.
# Locals imports.
from . import enums
from . import globals
from . import management

from .actions.actions import *
from .actions.talk import talk
from .inventory import Inventory
from .map import Map
from .player import Player
from .utils import clear, check_name, find_full_name, typewriter
from .world import *

# External imports.
import copy
import os
import random
import threading
from attrs import define, field
from datetime import datetime

import matplotlib

matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


@define
class Game:
    # Game variables.
    run: bool = field(default=True)
    menu: bool = field(default=True)
    play: bool = field(default=False)
    rules: bool = field(default=False)
    music: bool = field(default=True)
    settings: bool = field(default=False)
    first_setting: bool = field(default=False)
    loaded_game: bool = field(init=False)

    # Play variables.
    fight: bool = field(default=False)
    standing: bool = field(default=True)
    mapgame: Map = field(init=False)

    # Admin.
    admin: bool = field(default=False)

    # Existent player.
    existent_player: Player = field(init=False)
    player_name: str = field(init=False)

    # Settings.
    autosave: bool = field(default=False)
    music_volume: float = field(default=0.5)
    fadeout: int = field(default=2000)

    # Other.
    _last_fig = field(default=None)

    def __attrs_post_init__(self):
        # Init pygame music.
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.music_volume)

        # Game variables.
        self.loaded_game = False

        # Existent player.
        self.existent_player = management.import_player(path="./save/cfg_save.pkl")

    def show_intro(self) -> None:
        # Enter screen.
        displays.clear()
        displays.disp_intro()
        input()

    def show_menu(self) -> None:
        # Music background.
        self.play_music(filepath="./rsc/media/Echoes_of_the_Ancient_Lanes.mp3",
                        volume=self.music_volume,
                        bucle=True,
                        busy=True)

        # Main screen.
        displays.clear()
        displays.disp_title()
        displays.disp_main_screen()

        # Choice selection.
        selection = input(" # ")

        if selection == "1":
            self.show_new_game()
        if selection == "2":
            self.show_load_game()
        if selection == "3":
            self.show_rules()
        if selection == "4":
            self.show_settings()
        if selection == "0":
            self.close()

    def show_new_game(self) -> None:
        displays.clear()
        displays.disp_title()
        displays.disp_new_game(existent_player=self.existent_player)

        selection = ""
        if self.existent_player:
            selection = input(" # ")

        if self.existent_player is None or selection == "1":
            player_name = ""
            while not check_name(player_name):
                print()
                player_name = input(" # What's your NAME, hero? ").title()

            self.player_name = player_name

            self.menu = False
            self.play = True
            self.first_setting = True

    # TODO: refactorizar los últimos displays in place que hice en esta función.
    def show_load_game(self) -> None:
        displays.clear()
        displays.disp_title()
        displays.disp_load_game()

        typewriter(text=" Drifting through the veil of dreams... Please wait.",
                   speed=0.01)

        load_state, load_msg, player, map_game = management.load(check_hash=False)

        if load_state:
            self.loaded_game = load_state
            self.menu = False
            self.play = True
            self.existent_player = player
            self.mapgame = map_game

        if not load_state:
            print()
            print(load_msg)

        print()
        print()
        typewriter(text=f" Welcome back, {self.existent_player.name}. Your dream continues...",
                   speed=0.01)
        print()
        print()
        input(" > ")

    def main(self):
        self.show_intro()
        while self.run:
            if self.menu:
                self.show_menu()
            if self.rules:
                self.show_rules()
            if self.settings:
                self.show_settings()
            if self.play:
                self.show_play()
        self.close()

    # TODO: refactorizar los últimos displays in place que hice en esta función. Arriba del todo.
    def show_play(self):
        # Loading existent map.
        if self.loaded_game:
            player = self.existent_player
            map_game = self.mapgame
            self.first_setting = False

        # Introduction of new src.
        if self.first_setting:
            # First message.
            typewriter(
                text=f"\n   Okay, {self.player_name}, the dream is taking shape. You'll be inside in a few seconds.",
                speed=0.01)

            # Stop of background music.
            self.stop_music(fadeout=self.fadeout)

            # Initial settings.
            # Map settings.
            map_game = Map(items=copy.deepcopy(ITEMS),
                           quests=copy.deepcopy(QUESTS),
                           mobs=copy.deepcopy(MOBS),
                           biomes=copy.deepcopy(BIOMES),
                           regions=copy.deepcopy(REGIONS),
                           fishes=copy.deepcopy(FISHES),
                           npcs=copy.deepcopy(NPCS),
                           entries=copy.deepcopy(ENTRIES))

            # Player.
            player = Player(name=self.player_name,
                            place=map_game.map_settings[(12, 24)].entries["hut"],
                            last_place=map_game.map_settings[(12, 24)].entries["hut"],
                            last_entry=map_game.map_settings[(12, 24)].entries["hut"],
                            inventory=Inventory(item_base=ITEMS),
                            skills=[SKILLS["attack"]])

            # Preset of player.
            player.add_quest(quest=map_game.quests["quest_exit_the_hut"])
            player.add_quest(quest=map_game.quests["quest_firefrost_first_encounter"])
            player.add_item(item=copy.deepcopy(map_game.items["linen_shirt"]))
            player.add_item(item=copy.deepcopy(map_game.items["linen_trousers"]))
            player.add_item(item=copy.deepcopy(map_game.items["worn_boots"]))
            player.equip_item(item=player.get_item(item="linen_shirt"))
            player.equip_item(item=player.get_item(item="linen_trousers"))
            player.equip_item(item=player.get_item(item="worn_boots"))

            # Introduction setting.
            map_game.npcs["whispers"].messages = {
                0: [player.name + "...", player.name + "...",
                    "...your destiny awaits.",
                    "Follow the whispers of the wind, and come to me.",
                    "Secrets untold and challenges unknown lie ahead.",
                    "Trust in the unseen path...",
                    "... come to me."]}

            # Dragon Firefrost setting.
            map_game.npcs["dragon_firefrost"].messages = {
                0: [
                    player.name + "...",
                    "At last… after all this time, you stand before me again.",
                    "A thousand winters have passed, yet here you stand—unchanged in spirit.",
                    "Your stance… tense, cautious. Hm.",
                    "Your eyes… searching, wary...",
                    "... so this is how it must be.",
                    "Very well...",
                    "come...",
                    "let the valley witness our first clash in an age."
                    ]
            }

            # End message of setting.
            typewriter(text=f"\n\n   All set, {self.player_name}. The dream is live. Step in when you're ready.",
                       speed=0.01)
            input("\n\n   < PRESS ENTER >")

            # Introduction.
            if player.name and player.name.lower() != "tester":
                for _ in range(2):
                    displays.clear()
                    displays.disp_title()
                    print("\n" * 2)
                    print("    ")
                    displays.disp_narration()
                talk(npc=map_game.npcs["whispers"],
                     player=player,
                     mapgame=map_game)

        # Previous setting before start playing.
        # First screen massage.
        screen = random.choices(population=[msg.value for msg in enums.FirstMessages],
                                weights=[1, 1],
                                k=1)[0]

        # Music background.
        action = ["nothing"]

        # Set hours.
        hours = map_game.get_hours

        displays.clear()
        while self.play:
            # Time setting.
            time_init = datetime.now()

            # Event handler and map control.
            self.play, self.menu = management.event_handler(player=player,
                                                            mapgame=map_game,
                                                            time_init=time_init)
            management.map_control_handling(player=player,
                                            mapgame=map_game)

            # Map refresh.
            if not (map_game.get_hours == hours):
                # Map refresh.
                map_game.refresh_map(player=player, mapgame=map_game)

                # Player status refresh.
                player.refresh_temperature()
                player.refresh_temperature_status()
                player.refresh_buffs()
                player.refresh_status()
                if player.time_on:
                    player.refresh_hungry(hour=map_game.get_hours,
                                          last_hour=hours)
                    player.refresh_thirsty(hour=map_game.get_hours,
                                           last_hour=hours)
                    player.set_time_on()
                player.refresh_vital_energy(hour=map_game.get_hours,
                                            last_hour=hours)
            player.refresh_quests()

            # Setting reinit.
            if player.hp <= 0:
                management.reinit(player=player,
                                  mapgame=map_game)
                self.play, self.menu = False, True
                displays.disp_game_loss()

                management.save(player=player,
                                mapgame=map_game,
                                time_init=time_init)

            # Getting hours.
            hours = map_game.get_hours

            # Stop of music if not listen.
            if action[0] != "listen":
                self.stop_music(fadeout=self.fadeout)

            clear()

            # Fight chances of moving, and player status refreshing.
            if not player.standing:
                # Fight.
                if player.place.fight and player.place.mobs_respawned:
                    queue_mob = []
                    for mob in player.place.mobs_respawned:
                        if mob.should_attack(player=player):
                            queue_mob.append(mob)
                    if queue_mob:
                        number_enemies = min(1 + int(random.random() > 0.5), len(queue_mob))
                        enemies = random.sample(player.place.mobs_respawned, k=number_enemies)
                        win = battle(players=[player],
                                     mapgame=map_game,
                                     enemies=enemies)
                        if win:
                            enemies_names = [enemy.name for enemy in enemies]
                            screen += f"\n You battled width {' and '.join(enemies_names)}."

            if self.play and player.is_alive():
                # Draw of general stats.
                clear()
                displays.disp_play(player=player,
                                   mapgame=map_game,
                                   screen=screen,
                                   width=39)

                # Preset actions avaibles.
                actions, _ = player.get_available_actions(onbattle=False)
                actions_len = len(actions)

                # Input action.
                print()
                if not self.first_setting:
                    action = input(" " * 2 + "# ").lower().split()
                if self.first_setting:
                    map_game.add_hours(hours_to_add=1)
                    self.first_setting = False
                if not action:
                    action = ["None"]
                    player.standing = True

                # Action ejecution.
                if action[0] == "0":  # Save src.
                    self.play = False
                    self.menu = True
                    self.loaded_game = False
                    management.save(player=player, mapgame=map_game, time_init=time_init)

                if action[0] in ["1", "2", "3", "4"]:  # Move action.
                    if not player.move_available:
                        screen = "You're carrying too much weight to move."

                    elif player.outside:
                        screen, player.standing = move(player=player, map_game=map_game, mv=action[0])

                    else:
                        screen = "You are in " + player.place.get_name(month=map_game.current_month).title().replace(
                            "'S", "'s")

                elif action[0] in [f"{i}" for i in range(5, 4 + actions_len)]:
                    choice = int(action[0]) - 4

                    # TODO: implementar menu de skills y ejecución de la misma.
                    if actions[choice] == Actions.WAIT:
                        screen = "You have waited one hour."
                        map_game.add_hours(hours_to_add=1)
                        player.standing = True

                    if actions[choice] == Actions.SKILL:
                        screen = "Yet not implemented."
                        player.standing = True

                    if actions[choice] == Actions.USE_ITEM:
                        screen, _ = use(player=player,
                                        mapgame=map_game,
                                        item=player.equip[BodyPart.WAIST].slots_packs[
                                            choice - (actions_len - player.belt.slots)])
                    player.standing = True

                elif action[0] == "assign":  # Assign action.
                    quantity = 1
                    if len(action) < 2:
                        screen = displays.disp_assign(player.st_points)
                    if len(action) == 3:
                        quantity = 1
                        if action[2].isdigit():
                            quantity = int(action[2])
                    if len(action) >= 2 < 4:
                        screen = assign(player=player, stat=action[1], quantity=quantity)
                        player.standing = True

                elif action[0] == "attack":  # Attack action.
                    if len(action) == 1:
                        screen = displays.disp_attack()
                    else:
                        mob = find_full_name(partial_name=" ".join(action[1:]),
                                             names_list=[m.name.lower() for m in player.place.mobs_respawned])
                        if mob:
                            mob = player.place.get_mob(mob_id=MobTypes[underscores(mob)].value)
                            win = attack(player=player,
                                         map_game=map_game,
                                         mob=mob)

                            if win:
                                screen = f"You attacked {mob.name}."
                        else:
                            screen = f"There is no {' '.join(action[1:]).title()} here."
                    player.standing = True

                elif action[0] == "check":  # Check action.
                    if len(action) == 1:
                        screen = check(mapgame=map_game)

                    partial_name = "_".join(action[1:])
                    inventory = False
                    if "inv" in action or "inventory" in action:
                        inventory = True
                        partial_name = "_".join(action[2:])
                    keys = self.get_id_keys(entities=player.inventory.get_item_objects) + ["gold"]
                    keys.extend(self.get_id_keys(entities=player.place.get_trees_respawned()))
                    keys.extend(player.place.get_items())
                    keys.extend(self.get_id_keys(entities=player.place.get_mobs_respawned(), is_string=False))
                    target = find_full_name(partial_name=partial_name, names_list=keys)
                    screen = check(mapgame=map_game, player=player, target=target, inventory=inventory)

                elif action == ["draw", "map"]:  # Update of map action.
                    tower_of_eldra = map_game.map_settings[(34, 42)].entries["tower_of_eldra"].entries[
                        "tower_of_eldra_second_floor"]
                    tower_of_karun = map_game.map_settings[(14, 36)].entries["tower"].entries["second_floor"]
                    if player.place == tower_of_eldra:
                        exploration_radius = 10
                    elif player.place == tower_of_karun:
                        exploration_radius = 10
                    else:
                        exploration_radius = player.exploration_radius
                    player.standing = False
                    screen = draw_map(player=player, map_game=map_game, exploration_radius=exploration_radius)

                elif action[0] == "drink":
                    if len(action) == 1:
                        screen = "DRINK ITEM to drink something."
                    else:
                        item = find_full_name(partial_name="_".join(action[1:]),
                                              names_list=list(player.inventory.items.keys()),
                                              original=True)
                        screen = drink(player=player, item=item)
                        player.standing = False

                elif action[0] == "drop":  # Drop action.
                    try:  # Converting input in proper clases and form.
                        item = find_full_name(partial_name="_".join(action[2:]),
                                              names_list=list(player.inventory.items.keys()),
                                              original=True)

                        quantity = int(action[1])
                        screen = drop(player=player, item=item, quantity=quantity)  # Doing drop action.
                        player.standing = True

                    except ValueError:
                        screen = displays.disp_drop()  # Printing drop instructions.
                    except IndexError:
                        screen = displays.disp_drop()  # Printing drop instructions.

                elif action[0] == "eat":
                    item = find_full_name(partial_name="_".join(action[1:]),
                                          names_list=list(player.inventory.items.keys()),
                                          original=True)
                    if len(action) == 1:
                        screen = "EAT ITEM to eat something."
                    else:
                        screen = eat(player=player, item=item)
                        player.standing = False

                elif action[0] == "enter":  # Enter action.
                    if len(action) <= 2:
                        screen = displays.disp_enter(player.place)
                        player.standing = True

                    else:
                        entry_name = find_full_name(partial_name="_".join(action[2:]),
                                                    names_list=[*player.place.entries.keys()])
                        screen, player.standing = enter(player=player,
                                                        entrie=entry_name,
                                                        mapgame=map_game)

                elif action[0] in ["equip"] or action == ["show", "equip"]:  # Equip action.
                    if len(action) <= 1:
                        screen = displays.disp_equip(player.equip)
                        player.standing = True

                    else:
                        item = find_full_name(partial_name="_".join(action[1:]),
                                              names_list=list(player.inventory.items.keys()),
                                              original=True)
                        screen = equip(player=player,
                                       item=item)
                        player.standing = True

                elif action[0] == "exit":  # Exit entrie action:
                    screen, player.standing = exit_entry(player=player, map_game=map_game)

                elif action[0] == "explore":  # Explore action:
                    screen = explore(player=player, mapgame=map_game)
                    player.standing = False if player.outside else True

                elif action[0] == "fish":
                    screen = fish(player=player, mapgame=map_game)
                    player.standing = False

                elif action[0] == "land":  # Land action.
                    screen = land(player=player, map_game=map_game)
                    player.standing = False

                elif action[0] == "listen":  # Listen action.
                    entities = player.place.get_npc() + player.place.get_items()
                    entitie_name = find_full_name(partial_name="_".join(action[2:]).lower(),
                                                  names_list=entities,
                                                  original=True)
                    if len(action) <= 2:
                        screen = "What do you want to listen? LISTEN TO something."
                    else:
                        screen = listen(player=player,
                                        map_game=map_game,
                                        entitie=entitie_name)

                elif action == ["look", "around"]:  # Look around action.
                    look_around(player=player, map_game=map_game)
                    screen = displays.disp_look_around(player.place)
                    player.standing = False

                elif action[0] in ["map"] or action == ["show", "map"]:  # Show map.
                    player.map[player.y][player.x] = globals.PINK

                    zoom_size = 32 if not action[-1] == "all" else 128
                    half = zoom_size // 2 if not action[-1] == "all" else zoom_size
                    x_start = max(0, player.x - half)
                    x_end = min(127, player.x + half)
                    y_start = max(0, player.y - half)
                    y_end = min(127, player.y + half)
                    fig = plt.figure()
                    plt.imshow(player.map[y_start:y_end, x_start:x_end])
                    plt.title(player.name + "'s Map")
                    plt.show()
                    self._last_fig = fig

                    player.map[player.y][player.x] = map_game.map_settings[(player.x, player.y)].get_color(
                        month=map_game.current_month)
                    player.standing = True

                elif action[:2] == ["pick", "up"]:  # Pick up action.
                    item = find_full_name(partial_name="_".join(action[2:]),
                                          names_list=player.place.get_items(),
                                          original=True)
                    screen = pick_up(item=item, player=player, mapgame=map_game)

                elif action[0] == "read":  # Read action.
                    if len(action) <= 1:
                        screen = "If you want to read something use READ -ITEM."
                        player.standing = True

                    if len(action) > 1:
                        item = find_full_name(partial_name="_".join(action[1:]),
                                              names_list=player.place.get_items() + list(player.inventory.items.keys()),
                                              original=True)
                        screen = read(player=player, item=item)
                        player.standing = False

                elif action == ["show", "inventory"] or action[0] in ["inventory", "inv"]:
                    screen = displays.disp_show_inventory(player)
                    player.standing = True

                elif action[0] == "sleep":  # Sleep action.
                    if len(action) <= 2:
                        screen = displays.disp_sleep(player.place)
                        player.standing = True

                    else:
                        if action[2] in [tod.name.lower() for tod in enums.TimeOfDay]:
                            screen = sleep_in_bed(player=player,
                                                  map_game=map_game,
                                                  time_of_day=enums.TimeOfDay[action[2].upper()].value)
                            player.x_cp, player.y_cp = player.x, player.y
                            player.standing = True

                            # Autosave.
                            if self.autosave:
                                self.auto_save(player=player,
                                               mapgame=map_game,
                                               time_init=time_init)  # Autosave.

                        else:
                            screen = f"{action[2].title()} is not a time of day."
                            player.standing = True

                elif action[0] == "talk":  # Talk action.
                    npc_name = find_full_name(partial_name="_".join(action[2:]).lower(),
                                              names_list=player.place.get_npc(),
                                              original=True)

                    if len(action) <= 2:
                        screen = displays.disp_talk(player.place, mapgame=map_game)
                        player.standing = True

                    elif npc_name is None:
                        screen = "You need to specify the name more clearly."
                        player.standing = True

                    elif npc_name in player.place.get_npc():
                        screen = talk(npc=map_game.npcs[npc_name], player=player, mapgame=map_game)
                        player.standing = True

                    else:
                        screen = f"Here no one is called {npc_name.replace('_', ' ').title()}."
                        player.standing = True

                elif action[0] == "unequip":  # Unequip action.
                    if len(action) <= 1:
                        screen = displays.disp_equip(player.equip)
                        player.standing = True

                    else:
                        item = find_full_name(partial_name="_".join(action[1:]).replace("'", ""),
                                              names_list=[i.id for i in player.get_equiped_items()],
                                              unique=False,
                                              original=True)
                        screen = unequip(player=player, item=item)
                        player.standing = True

                elif action == ["use", "boat"]:  # Use boat action.
                    screen = use_boat(player=player, map_game=map_game)
                    player.standing = True

                elif action[0] == "use":  # Use object action.
                    if len(action) == 1:
                        screen = displays.disp_use()
                    else:
                        item = find_full_name(partial_name="_".join(action[1:]),
                                              names_list=list(player.inventory.items.keys()),
                                              unique=False,
                                              original=True)
                        screen, _ = use(player=player,
                                        mapgame=map_game,
                                        item=item)
                        player.standing = True

                elif action[0] == "wait":  # Wait action.
                    if len(action) <= 2:
                        screen = displays.disp_wait()
                        player.standing = True

                    else:
                        if action[2] in [tod.name.lower() for tod in enums.TimeOfDay]:
                            screen = wait(map_game=map_game,
                                          time_of_day=enums.TimeOfDay[action[2].upper()].value)
                            player.standing = False
                        else:
                            screen = f"{action[2].title()} is not a time of day."
                            player.standing = True

                # -------- admin commans.
                if action[0] == "poweradmin":
                    self.admin = True

                if action == ["fenix", "recover"]:
                    player.heal(amount=9999)
                    player.recover_vital_energy(amount=9999)

                if action == ["player", "active", "vital", "energy"]:
                    player.active_vital_energy()
                    screen = "Vital energy was activated."

                if self.admin or player.name == "Tester":
                    if action[:2] == ["dragon", "fortune"]:
                        quantity_item = int(action[3]) if len(action) == 4 else 1
                        player.add_item(item=map_game.get_item_object(item_id=action[2]), quantity=quantity_item)

                    elif action[0] == "estimate":
                        screen = f"{map_game.estimate_date(days=int(action[1]))}"

                    elif action[:2] == ["dict", "player"]:
                        if len(action) == 3:
                            try:
                                screen = f"{getattr(player, action[2])}"
                            except AttributeError:
                                screen = f"Acces to: Player -> {action[2]} not posible."
                        if len(action) == 4:
                            try:
                                screen = f"{getattr(getattr(player, action[2]), action[3])}"
                            except AttributeError:
                                screen = f"Acces to: Player -> {action[2]} -> {action[3]} not posible."

                    elif action[:2] == ["lvl", "up"]:
                        if len(action) == 2:
                            quantity = 1
                        else:
                            quantity = int(action[2])
                        player.lvl_up(quantity=quantity)
                        screen = f"You have lvl up {quantity} levels."

                    elif action[:2] == ["add", "skill"]:
                        if action[2] in SKILLS.keys():
                            player.add_skill(SKILLS[action[2]])
                            screen = f"{underscores(text=action[2], delete=True).title()} has been learned."
                        else:
                            screen = "Not valid skill."

                    elif action[0] == "precision":
                        screen = f"{player.precision}"

                    elif action[0] == "teleport":
                        player.set_place(map_game.map_settings[(int(action[1]), int(action[2]))])
                        screen = f"You have teleported to {action[1]} {action[2]}."

                    elif action[:2] == ["time", "travel"]:
                        map_game.add_days(days_to_add=int(action[2]))
                        screen = f"You have time travel to {action[2]} days."

                    elif action[:2] == ["mob", "quantity"]:
                        screen = f"There {len(player.place.mobs_respawned)} mobs."

                    elif action[:2] == ["remove", "mob"]:
                        player.place.remove_mob_respawned(mob_id=int(action[2]))
                        screen = f"There {len(player.place.mobs_respawned)} mobs."

                    elif action == ["dragon", "vision"]:
                        player.vision = 1000
                        screen = f"Now you have god vision."

                    elif action[:2] == ["dict", "map"]:
                        if len(action) == 3:
                            try:
                                screen = f"{getattr(map_game, action[2])}"
                            except AttributeError:
                                screen = f"Acces to: Map -> {action[2]} not posible."
                        if len(action) == 4:
                            try:
                                screen = f"{getattr(getattr(map_game, action[2]), action[3])}"
                            except AttributeError:
                                screen = f"Acces to: Map -> {action[2]} -> {action[3]} not posible."

                    elif action[:2] == ["gen", "battle"]:
                        e = []
                        for mob in action[2:]:
                            if mob in MOBS.keys():
                                e.append(copy.deepcopy(MOBS[mob]))
                        if e:
                            battle(players=[player], enemies=e, mapgame=map_game)

                    elif action == ["active", "moves"]:
                        screen = f"{map_game.get_avaible_moves(player=player)}"

                    elif action[:2] == ["count", "biome"]:
                        screen = f"{map_game.get_number_biomes(biome_id=action[2:])}"

                    elif action[:2] == ["count", "mob"]:
                        screen = "Command must recive: COUNT MOB COORD1 COORD2 MOB_ID"
                        if not len(action) < 5:
                            screen = f"{map_game.get_number_of_mobs(coord1=eval(action[2]), coord2=eval(action[3]), mob_id=action[4])}"

                    elif action == ["region", "labels"]:
                        print(map_game.region_labels)
                        input()
                        screen = "Region labels shown."

                    elif action[0] == "update":
                        opt = "_".join(action[1:])
                        screen, player, map_game = management.update(player=player, mapgame=map_game, option=opt)

                    elif action[0] == "equal":
                        npc_quest = map_game.npcs['ant_loial'].get_first_quest()
                        player_quest = player.quests_in_progress[0]
                        screen = f"Equal: {player_quest == npc_quest}, {player_quest is npc_quest}, {id(player_quest)}, {id(npc_quest)}"
            else:
                player.standing = True

    def events(self):
        pass

    def show_rules(self):
        displays.clear()
        displays.disp_title()
        displays.disp_rules()
        self.rules = False
        input(" > ")

    def show_settings(self):
        pass

    @staticmethod
    def close():
        exit()

    @staticmethod
    def auto_save(player: Player,
                  mapgame: Map,
                  time_init: datetime) -> None:
        thread = threading.Thread(
            target=management.save,
            args=(player, mapgame, time_init))
        thread.daemon = True
        thread.start()

    @staticmethod
    def play_music(filepath: str,
                   volume: float = globals.MUSIC_VOLUME,
                   bucle: bool = False,
                   busy: bool = False) -> None:
        if busy:
            if pygame.mixer.music.get_busy():
                return
        pygame.mixer.music.load(filename=filepath)
        pygame.mixer.music.set_volume(volume)
        if bucle:
            pygame.mixer.music.play(-1)

    @staticmethod
    def stop_music(fadeout: int = 0) -> None:
        if fadeout:
            pygame.mixer.music.fadeout(fadeout)
            return
        pygame.mixer.music.stop()

    @staticmethod
    def set_music_volume(volume: float) -> None:
        pygame.mixer.music.set_volume(volume=volume)

    @staticmethod
    def get_id_keys(entities: list, is_string: bool = True):
        if is_string:
            return [entitie.id for entitie in entities]
        return [entitie.id_key for entitie in entities]


if __name__ == "__main__":
    game = Game(autosave=True)
    game.main()
    game.close()
