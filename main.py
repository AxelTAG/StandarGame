# Imports.
# Locals imports.
import enums
import globals
import management

from actions import *
from inventory import Inventory
from map import Map
from player import Player
from utils import draw_move, clear, check_name, find_full_name, typewriter
from world import *

# External imports.
import copy
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import os
import random
import threading
from attrs import define, field
from datetime import datetime

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
        if selection == "5":
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

        # Introduction of new game.
        if self.first_setting:
            # First message.
            typewriter(
                text=f"\n   Okay, {self.player_name}, the dream is taking shape. You'll be inside in a few seconds.",
                speed=0.01)

            # Stop of background music.
            self.stop_music(fadeout=self.fadeout)

            # Initial settings.
            # Map settings.
            map_game = Map(mobs=copy.deepcopy(MOBS),
                           biomes=copy.deepcopy(BIOMES),
                           npcs=copy.deepcopy(NPCS),
                           entries=copy.deepcopy(ENTRIES))

            # Player.
            player = Player(name=self.player_name,
                            place=map_game.map_settings[(12, 24)].entries["hut"],
                            last_place=map_game.map_settings[(12, 24)].entries["hut"],
                            last_entry=map_game.map_settings[(12, 24)].entries["hut"],
                            inventory=Inventory(item_base=ITEMS))

            # Location setting.
            map_game.map_settings[(12, 24)].entries["hut"].name = player.name + "'s Hut"

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
                0: [player.name + "...", "You finally come to me...",
                    "Destiny calls for a dance of fire and frost between us...",
                    "Ready your blade..."]}

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
                    typewriter(text=f" . . .",
                               speed=0.3)
                screen = talk(npc=map_game.npcs["whispers"],
                              player=player,
                              map_game=map_game)

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

            if not (map_game.get_hours == hours):
                # Map refresh.
                map_game.refresh_npcs()
                map_game.refresh_biomes()

                # Player status refresh.
                player.refresh_status()
                player.refresh_hungry(hour=map_game.get_hours,
                                      last_hour=hours)
                player.refresh_thirsty(hour=map_game.get_hours,
                                       last_hour=hours)

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
                    if random.randint(a=0, b=100) < max(player.place.get_mobs_chances(map_game.current_month)):

                        enemy = random.choices(player.place.mobs_respawned, k=1)[0]
                        self.play, self.menu, win = battle(player=player,
                                                           map_game=map_game,
                                                           enemy=enemy)
                        if win:
                            screen += f"\n You battled width {enemy.name}."

            if self.play:
                # Draw of general stats.
                clear()
                displays.disp_play(player=player,
                                   map_game=map_game,
                                   reg="NAIWAT",
                                   x=player.x,
                                   y=player.y,
                                   mdir=draw_move(x=player.x,
                                                  y=player.y,
                                                  mapgame=map_game,
                                                  map_height=map_game.x_len,
                                                  map_width=map_game.y_len,
                                                  player=player,
                                                  tl_map=map_game.map_labels,
                                                  ms=map_game.map_settings),
                                   screen_text=screen,
                                   width=38)

                # Input action.
                print()
                action = input(" " * 2 + "# ").lower().split()
                if not action:
                    action = ["None"]
                    player.standing = True

                # Action ejecution.
                if action[0] == "0":  # Save game.
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
                        screen = "You are in " + player.place.get_name(month=map_game.current_month).title().replace("'S", "'s")

                elif action[0] in ["5", "6"]:  # Fast use object action.
                    if action[0] == "5":
                        screen, _ = use(player=player, map_game=map_game, item=player.slot1)
                    if action[0] == "6":
                        screen, _ = use(player=player, map_game=map_game, item=player.slot2)
                    player.standing = True

                elif action[0] == "assign":  # Assign action.
                    if len(action) < 2:
                        screen = displays.disp_assign(player.st_points)
                    elif player.st_points:
                        if action[1] in ["strength", "str"]:
                            player.strength += 1
                            player.st_points -= 1
                            screen = "You have assigned a skill point to strength."
                        elif action[1] in ["agility", "agi"]:
                            player.agility += 1
                            player.st_points -= 1
                            screen = "You have assigned a skill point to agility."
                        elif action[1] in ["resistance", "res"]:
                            player.resistance += 1
                            player.st_points -= 1
                            screen = "You have assigned a skill point to resistance."
                        elif action[1] in ["vitality", "vit"]:
                            player.vitality += 1
                            player.st_points -= 1
                            screen = "You have assigned a skill point to vitality."
                    elif player.st_points == 0:
                        screen = "You have no more skill points left."
                    else:
                        "That is not posible."
                    player.standing = True

                elif action[0] == "attack":  # Attack action.
                    if len(action) == 1:
                        screen = displays.disp_attack()
                    else:
                        mob = find_full_name(partial_name=" ".join(action[1:]),
                                             names_list=[m.name.lower() for m in player.place.mobs_respawned])
                        if mob:
                            mob = player.place.get_mob(mob_id=MobTypes[underscores(mob)].value)
                            _, _, win = attack(player=player,
                                               map_game=map_game,
                                               mob=mob)

                            if win:
                                screen = f"You attacked {mob.name}."
                        else:
                            screen = f"There is no {' '.join(action[1:]).title()} here."
                    player.standing = True

                elif action[0] == "check":  # Check action.
                    if len(action) == 1:
                        screen = check(player=player, item=" ".join(action[1:]))

                    elif action[1] in ["inv", "inventory"]:
                        item = find_full_name(partial_name="_".join(action[2:]),
                                              names_list=list(player.inventory.items.keys()))
                        screen = check(player=player, item=item, inventory=True)

                    else:
                        item = find_full_name(partial_name="_".join(action[1:]),
                                              names_list=player.place.get_items())
                        screen = check(player=player, item=item)

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
                    screen = explore(player=player, map_game=map_game)
                    player.standing = False if player.outside else True

                elif action[0] == "fish":
                    screen = fish(player=player, map_game=map_game)
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

                    player.map[player.y][player.x] = map_game.map_settings[(player.x, player.y)].get_color(month=map_game.current_month)
                    player.standing = True

                elif action[:2] == ["pick", "up"]:  # Pick up action.
                    item = find_full_name(partial_name="_".join(action[2:]),
                                          names_list=player.place.get_items(),
                                          original=True)
                    screen = pick_up(player=player, item=item)

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

                elif action[0] == "slot1":  # Selection slot1 action.
                    item_select = "_".join(action[1:])
                    item_object = get_item(item_name=item_select)
                    if (
                            item_object.consumable or item_object.equippable) and item_select in player.inventory.items.keys():
                        player.slot1 = item_select
                    else:
                        screen = f"You cannot equip {item_object.name} in the belt."
                    player.standing = True

                elif action[0] == "slot2":  # Selection slot1 action.
                    item_select = "_".join(action[1:])
                    item_object = get_item(item_name=item_select)
                    if item_object.consumable or item_object.equippable and item_select in player.inventory.items.keys():
                        player.slot2 = item_select
                    else:
                        screen = f"You cannot equip {item_object.name} in the belt."
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
                        screen = talk(npc=map_game.npcs[npc_name], player=player, map_game=map_game)
                        player.standing = True

                    else:
                        screen = f"Here no one is called {npc_name.replace('_', ' ').title()}."
                        player.standing = True

                elif action[0] == "unequip":  # Unequip action.
                    if len(action) <= 1:
                        screen = displays.disp_equip(player.equip)
                        player.standing = True

                    else:
                        item = find_full_name(partial_name="_".join(action[1:]),
                                              names_list=[underscores(i.name) for i in player.equip.values() if
                                                          i is not None],
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
                                        map_game=map_game,
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

                # --- admin commans.
                if action[0] == "poweradmin":
                    self.admin = True

                if self.admin:
                    if action[0] == "events":
                        screen = f"{player.events}"

                    elif action[0] == "estimate":
                        screen = f"{map_game.estimate_date(days=int(action[1]))}"

                    elif action[:2] == ["dict", "player"]:
                        if len(action) == 3:
                            screen = f"{getattr(player, action[2])}"
                        if len(action) == 4:
                            screen = f"{getattr(getattr(player, action[2]), action[3])}"

                    elif action[:2] == ["lvl", "up"]:
                        if len(action) == 2:
                            quantity = 1
                        else:
                            quantity = int(action[2])
                        player.lvl_up(quantity=quantity)
                        screen = f"You have lvl up {quantity} levels."

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

                    elif action[0] == "update":
                        opt = "_".join(action[1:])
                        screen, player, map_game = management.update(player=player, mapgame=map_game, option=opt)

                    elif action[0] == "repair":
                        map_game.map_settings[(36, 42)].entries = {
                            "cave": map_game.map_settings[(49, 43)].entries["cave"]
                        }
                        map_game.map_settings[(36, 42)].entries["cave"].leave_entry = map_game.map_settings[
                            (36, 42)]
                        screen = "Game repaired."
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


if __name__ == "__main__":
    game = Game(autosave=True)
    game.main()
    game.close()
